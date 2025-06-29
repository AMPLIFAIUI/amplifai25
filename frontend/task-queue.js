// Task queue management
class TaskQueue {
    constructor() {
        this.queue = [];
        this.processing = false;
        this.maxConcurrent = 5;
        this.currentTasks = new Set();
    }

    async processQueue() {
        if (this.processing) return;
        this.processing = true;

        while (this.queue.length > 0 && this.currentTasks.size < this.maxConcurrent) {
            const task = this.queue.shift();
            this.currentTasks.add(task);
            task().finally(() => {
                this.currentTasks.delete(task);
                this.processQueue();
            });
        }

        this.processing = false;
    }

    async addTask(task) {
        this.queue.push(task);
        this.processQueue();
    }

    predictiveSchedule(tasks) {
        tasks.sort((a, b) => b.priority - a.priority);
        tasks.forEach(task => this.addTask(task));
    }
}