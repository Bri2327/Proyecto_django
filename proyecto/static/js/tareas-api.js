class TasksAPI {
    constructor() {
        this.baseURL = '/proyecto/';
    }

    request = async (endpoint, options = {}) => {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Error en API call a ${endpoint}:`, error);
            throw error;
        }
    }

    getStatistics = async () => this.request('tasks-statistics')

    getPeople = async () => this.request('person')

    getTasksByPerson = async (personId, estado = null) => {
        let endpoint = `person/${personId}/tasks`;
        if (estado) {
            endpoint += `?state=${encodeURIComponent(estado)}`;
        }
        return this.request(endpoint);
    }

    getAllTasks = async (estado = null) => {
        try {
            let endpoint = 'all-tasks';
            if (estado) {
                endpoint += `?state=${encodeURIComponent(estado)}`;
            }
            
            const data = await this.request(endpoint);
            
            const transformedTasks = data.tareas_asignadas.map(task => ({
                ...task,
                person_name: `${task.persona.nombre} ${task.persona.apellido}`,
                person_id: task.persona.id
            }));
            
            return transformedTasks;
        } catch (error) {
            console.error('Error getting all tasks:', error);
            throw error;
        }
    }
}

const tasksAPI = new TasksAPI();
