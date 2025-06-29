```js js/amp-memory.js
class AmpMemory {
    constructor(maxChats = 5) {
        this.maxChats = maxChats;
        this.chats = JSON.parse(localStorage.getItem('ampChats')) || [];
    }
    addChat(chat) {
        this.chats.unshift(chat);
        if (this.chats.length > this.maxChats) this.chats.pop();
        localStorage.setItem('ampChats', JSON.stringify(this.chats));
    }
    getChats() {
        return this.chats;
        }
    }
```