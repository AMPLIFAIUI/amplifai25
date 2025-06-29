// AMPLIFAI Settings Manager

export default class SettingsManager {
    constructor(storageKey = 'amplifai-settings') {
        this.storageKey = storageKey;
        this.settings = this.loadSettings();
    }

    loadSettings() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (saved) return JSON.parse(saved);
        } catch (e) { }
        return {
            general: { instanceName: 'My Amp', autoStart: false, language: 'en', theme: 'light', updateChannel: 'stable' },
            security: { encryptionLevel: 'high', e2eEncryption: true, passwordProtection: false, autoLock: true, lockTimeout: 15 },
            folders: { allowed: [], denied: [] },
            sync: { enabled: true, interval: 10, cloudProvider: 'dropbox' },
            appearance: { fontSize: 16, colorScheme: 'default' },
            automation: { rules: [] }
        };
    }

    saveSettings() {
        try { localStorage.setItem(this.storageKey, JSON.stringify(this.settings)); } catch (e) { }
    }

    updateSetting(section, key, value) {
        if (this.settings[section]) {
            this.settings[section][key] = value;
            this.saveSettings();
        }
    }

    getSetting(section, key) {
        return this.settings[section] ? this.settings[section][key] : undefined;
    }

    resetSettings() {
        localStorage.removeItem(this.storageKey);
        this.settings = this.loadSettings();
        this.saveSettings();
    }

    render(container) {
        container.innerHTML = `<h2>Settings</h2>
        <pre>${JSON.stringify(this.settings, null, 2)}</pre>
        <button id="close-settings">Close</button>`;
        document.getElementById('close-settings').onclick = () => container.classList.remove('active');
    }
}