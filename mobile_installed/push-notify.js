// Request notification permission and subscribe to push
async function subscribeUser() {
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    try {
      const reg = await navigator.serviceWorker.ready;
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        // Subscribe to push (public VAPID key needed for real use)
        let sub;
        try {
          sub = await reg.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: 'YOUR_PUBLIC_VAPID_KEY_HERE'
          });
        } catch (err) {
          alert('Failed to subscribe to push notifications: ' + err);
          return;
        }
        // Send sub to backend (implement this endpoint)
        try {
          await fetch('/api/subscribe-push', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(sub)
          });
          alert('Push notifications enabled!');
        } catch (err) {
          alert('Failed to send subscription to backend: ' + err);
        }

        // Show a test notification immediately
        if (reg.showNotification) {
          reg.showNotification('Test Notification', {
            body: 'Notifications are working!',
            icon: 'icon-192.png',
            badge: 'icon-192.png'
          });
        } else if (window.Notification) {
          new Notification('Test Notification', {
            body: 'Notifications are working!',
            icon: 'icon-192.png',
            badge: 'icon-192.png'
          });
        }
      } else {
        alert('Notifications denied.');
      }
    } catch (err) {
      alert('Error during push setup: ' + err);
    }
  }
}
