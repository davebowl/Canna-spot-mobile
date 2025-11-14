// Request notification permission and subscribe to push
async function subscribeUser() {
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    const reg = await navigator.serviceWorker.ready;
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      // Subscribe to push (public VAPID key needed for real use)
      const sub = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: 'YOUR_PUBLIC_VAPID_KEY_HERE'
      });
      // Send sub to backend (implement this endpoint)
      await fetch('/api/subscribe-push', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(sub)
      });
      alert('Push notifications enabled!');
    } else {
      alert('Notifications denied.');
    }
  }
}
