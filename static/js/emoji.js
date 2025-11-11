// Insert emoji into target input/textarea at cursor position
function insertEmoji(emoji, targetEl) {
  if (!targetEl) return;
  const isTextarea = targetEl.tagName === 'TEXTAREA';
  const start = targetEl.selectionStart || targetEl.value.length;
  const end = targetEl.selectionEnd || targetEl.value.length;
  targetEl.value = targetEl.value.substring(0, start) + emoji + targetEl.value.substring(end);
  targetEl.focus();
  targetEl.setSelectionRange(start + emoji.length, start + emoji.length);
  // Trigger input event for any listeners
  targetEl.dispatchEvent(new Event('input', { bubbles: true }));
}

// Common emoji sets
const emojiGroups = {
  smileys: ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', '😉', '😊', '😇', '🥰', '😍', '🤩', '😘', '😗', '😚', '😙', '🥲', '😋', '😛', '😜', '🤪', '😝', '🤑', '🤗', '🤭', '🤫', '🤔', '🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥', '😌', '😔', '😪', '🤤', '😴'],
  nature: ['🌿', '🍀', '🌱', '🌲', '🌳', '🌴', '🌵', '🌾', '🌺', '🌻', '🌼', '🌷', '🌸', '💐', '🥀', '🌹', '🏵️', '🍁', '🍂', '🍃', '☘️', '🪴'],
  cannabis: ['🌿', '🍃', '💨', '🔥', '💚', '🌱', '🪴', '🍀', '☘️'],
  food: ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🫐', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌶️', '🫑', '🌽', '🥕', '🫒', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳'],
  symbols: ['❤️', '💚', '💛', '🧡', '💜', '🖤', '🤍', '🤎', '💙', '💗', '💖', '💕', '💞', '💓', '💝', '✨', '⭐', '🌟', '💫', '⚡', '🔥', '💯', '✅', '👍', '👎', '👌', '🤘', '🤙', '👏', '🙌']
};

// Load custom emojis from backend and merge
let customEmojisLoaded = false;
async function loadCustomEmojis() {
  try {
    const res = await fetch('/api/emojis');
    const data = await res.json();
    if (data.success && data.emojis) {
      // Merge custom emojis with defaults
      Object.keys(data.emojis).forEach(cat => {
        if (emojiGroups[cat]) {
          // Add to existing category
          data.emojis[cat].forEach(emojiData => {
            // emojiData can be {char: '😀'} or {image: '/uploads/...', label: 'Custom'}
            if (typeof emojiData === 'string') {
              // Old format compatibility
              if (!emojiGroups[cat].includes(emojiData)) {
                emojiGroups[cat].push(emojiData);
              }
            } else {
              // New format with char or image
              emojiGroups[cat].push(emojiData);
            }
          });
        } else {
          // Create new category
          emojiGroups[cat] = data.emojis[cat];
        }
      });
      customEmojisLoaded = true;
    }
  } catch (e) {
    console.warn('[emoji] Failed to load custom emojis:', e);
    customEmojisLoaded = true; // Mark as attempted
  }
}

// Call on page load
loadCustomEmojis();

// Create and show emoji picker
function addEmojiPicker(button, targetInput) {
  if (!button || !targetInput) return;
  
  let picker = null;
  
  button.addEventListener('click', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    // Wait for custom emojis if not loaded yet
    if (!customEmojisLoaded) {
      await loadCustomEmojis();
    }
    
    // Toggle picker
    if (picker && picker.parentNode) {
      picker.remove();
      picker = null;
      return;
    }
    
    // Create picker
    picker = document.createElement('div');
    picker.className = 'emoji-picker';
    picker.style.cssText = `
      position: absolute;
      background: var(--card);
      border: 1px solid var(--green);
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
      z-index: 1000;
      max-width: 320px;
      max-height: 300px;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
    `;
    
    // Position picker (mobile-aware)
    const rect = button.getBoundingClientRect();
    const isMobile = window.innerWidth < 640;
    if (isMobile) {
      // Center on mobile
      picker.style.left = '50%';
      picker.style.transform = 'translateX(-50%)';
      picker.style.bottom = '80px';
      picker.style.position = 'fixed';
      picker.style.maxWidth = '90vw';
    } else {
      picker.style.right = '0';
      picker.style.top = (rect.bottom + 5) + 'px';
    }
    
    // Build emoji tabs dynamically from available groups
    const tabBar = document.createElement('div');
    tabBar.style.cssText = 'display:flex;gap:8px;margin-bottom:8px;border-bottom:1px solid rgba(0,255,153,0.3);padding-bottom:8px;overflow-x:auto;-webkit-overflow-scrolling:touch';
    
    // Predefined tab order with icons
    const tabIcons = {
      smileys: '😀',
      cannabis: '🌿',
      nature: '🌱',
      food: '�',
      symbols: '❤️',
      custom: '⭐'
    };
    
    // Build tabs from available emoji groups
    const tabs = [];
    Object.keys(emojiGroups).forEach(groupName => {
      tabs.push({
        name: groupName,
        icon: tabIcons[groupName] || emojiGroups[groupName][0] || '📁',
        label: groupName.charAt(0).toUpperCase() + groupName.slice(1)
      });
    });
    
    const emojiGrid = document.createElement('div');
    emojiGrid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fill,minmax(36px,1fr));gap:4px';
    
    function showGroup(groupName) {
      emojiGrid.innerHTML = '';
      (emojiGroups[groupName] || []).forEach(emojiData => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.style.cssText = 'font-size:24px;padding:6px;border:1px solid transparent;background:transparent;cursor:pointer;border-radius:6px;transition:all 0.2s;min-width:36px;min-height:36px;display:flex;align-items:center;justify-content:center';
        
        // Handle both string emojis and object {char: '😀'} or {image: 'url'}
        let emojiValue;
        if (typeof emojiData === 'string') {
          // Plain emoji character
          btn.textContent = emojiData;
          emojiValue = emojiData;
        } else if (emojiData.char) {
          // Emoji object with character
          btn.textContent = emojiData.char;
          emojiValue = emojiData.char;
          if (emojiData.label) btn.title = emojiData.label;
        } else if (emojiData.image) {
          // Custom emoji image
          const img = document.createElement('img');
          img.src = emojiData.image;
          img.alt = emojiData.label || 'emoji';
          img.style.cssText = 'width:28px;height:28px;object-fit:contain;pointer-events:none';
          btn.appendChild(img);
          emojiValue = `![${emojiData.label || 'emoji'}](${emojiData.image})`;
          if (emojiData.label) btn.title = emojiData.label;
        }
        
        btn.addEventListener('mouseenter', () => {
          btn.style.background = 'var(--soft)';
          btn.style.borderColor = 'var(--green)';
        });
        btn.addEventListener('mouseleave', () => {
          btn.style.background = 'transparent';
          btn.style.borderColor = 'transparent';
        });
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          insertEmoji(emojiValue, targetInput);
          picker.remove();
          picker = null;
        });
        emojiGrid.appendChild(btn);
      });
    }
    
    tabs.forEach((tab, idx) => {
      const tabBtn = document.createElement('button');
      tabBtn.textContent = tab.icon;
      tabBtn.title = tab.label;
      tabBtn.type = 'button';
      tabBtn.style.cssText = 'font-size:20px;padding:6px 10px;border:1px solid transparent;background:transparent;cursor:pointer;border-radius:6px;min-width:40px;transition:all 0.2s;flex-shrink:0';
      if (idx === 0) {
        tabBtn.style.background = 'var(--soft)';
        tabBtn.style.borderColor = 'var(--green)';
      }
      tabBtn.addEventListener('click', (e) => {
        e.preventDefault();
        // Clear all tab highlights
        Array.from(tabBar.children).forEach(t => {
          t.style.background = 'transparent';
          t.style.borderColor = 'transparent';
        });
        tabBtn.style.background = 'var(--soft)';
        tabBtn.style.borderColor = 'var(--green)';
        showGroup(tab.name);
      });
      tabBar.appendChild(tabBtn);
    });
    
    picker.appendChild(tabBar);
    picker.appendChild(emojiGrid);
    
    // Show first group
    showGroup('smileys');
    
    // Append to form or body
    const form = targetInput.closest('form') || document.body;
    if (form.style.position !== 'relative' && form.style.position !== 'absolute') {
      form.style.position = 'relative';
    }
    form.appendChild(picker);
    
    // Close on outside click
    setTimeout(() => {
      const closeHandler = (e) => {
        if (picker && !picker.contains(e.target) && e.target !== button) {
          picker.remove();
          picker = null;
          document.removeEventListener('click', closeHandler);
        }
      };
      document.addEventListener('click', closeHandler);
    }, 100);
  });
}

// Legacy support for old insertEmoji signature
window.insertEmoji = (emoji) => {
  const target = document.querySelector('input[name="content"]') || document.getElementById('msg') || document.getElementById('commentText');
  insertEmoji(emoji, target);
};

// Expose for use in templates
window.addEmojiPicker = addEmojiPicker;
