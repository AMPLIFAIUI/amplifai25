// User-centric plug memory (encrypted, modifiable via UI only)

class UserProfile {
    constructor(userId) {
        this.userId = userId;
        this.data = this.loadProfile();
    }

    loadProfile() {
        // Load from encrypted store or localStorage
    }

    saveProfile() {
        // Save to encrypted store or localStorage
    }

    updatePreferences(prefs) {
        this.data.preferences = { ...this.data.preferences, ...prefs };
        this.saveProfile();
    }

    getPreferences() {
        return this.data.preferences;
    }
}

module.exports = UserProfile;