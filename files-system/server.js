const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const marked = require('marked');

const app = express();
const PORT = 3003;
const WORKSPACE_ROOT = '/root/.openclaw/workspace';

app.use(express.json());
app.use(express.static(__dirname));

// Security: Validate and normalize paths
function validatePath(userPath) {
  const normalized = path.normalize(userPath || '');
  const fullPath = path.join(WORKSPACE_ROOT, normalized);
  
  // Prevent path traversal
  if (!fullPath.startsWith(WORKSPACE_ROOT)) {
    throw new Error('Invalid path');
  }
  
  return fullPath;
}

// List files and folders
app.get('/api/files', async (req, res) => {
  try {
    const relativePath = req.query.path || '';
    const fullPath = validatePath(relativePath);
    
    const items = await fs.readdir(fullPath, { withFileTypes: true });
    const fileList = await Promise.all(
      items.map(async (item) => {
        const itemPath = path.join(fullPath, item.name);
        const stats = await fs.stat(itemPath);
        
        return {
          name: item.name,
          isDirectory: item.isDirectory(),
          size: stats.size,
          modified: stats.mtime,
          path: path.join(relativePath, item.name)
        };
      })
    );
    
    // Sort: directories first, then files
    fileList.sort((a, b) => {
      if (a.isDirectory && !b.isDirectory) return -1;
      if (!a.isDirectory && b.isDirectory) return 1;
      return a.name.localeCompare(b.name);
    });
    
    res.json({
      currentPath: relativePath,
      items: fileList
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get file content
app.get('/api/file/content', async (req, res) => {
  try {
    const relativePath = req.query.path || '';
    const fullPath = validatePath(relativePath);
    
    const stats = await fs.stat(fullPath);
    if (stats.isDirectory()) {
      return res.status(400).json({ error: 'Path is a directory' });
    }
    
    const ext = path.extname(fullPath).toLowerCase();
    const content = await fs.readFile(fullPath, 'utf-8');
    
    let response = {
      name: path.basename(fullPath),
      path: relativePath,
      size: stats.size,
      modified: stats.mtime,
      content: content,
      type: 'text'
    };
    
    // Render markdown
    if (ext === '.md') {
      response.type = 'markdown';
      response.html = marked.parse(content);
    }
    
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Download file
app.get('/api/file/download', async (req, res) => {
  try {
    const relativePath = req.query.path || '';
    const fullPath = validatePath(relativePath);
    
    const stats = await fs.stat(fullPath);
    if (stats.isDirectory()) {
      return res.status(400).json({ error: 'Cannot download directory' });
    }
    
    res.download(fullPath, path.basename(fullPath));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete files/folders
app.delete('/api/files', async (req, res) => {
  try {
    const { paths } = req.body;
    
    if (!Array.isArray(paths) || paths.length === 0) {
      return res.status(400).json({ error: 'No paths provided' });
    }
    
    const results = [];
    
    for (const relativePath of paths) {
      try {
        const fullPath = validatePath(relativePath);
        await fs.rm(fullPath, { recursive: true, force: true });
        results.push({ path: relativePath, success: true });
      } catch (error) {
        results.push({ path: relativePath, success: false, error: error.message });
      }
    }
    
    res.json({ results });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Files server running on port ${PORT}`);
});
