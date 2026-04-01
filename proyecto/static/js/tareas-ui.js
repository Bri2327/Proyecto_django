class TasksUI {
  constructor() {
    this.tasks = [];
    this.people = [];
    this.init();
  }

  init = () => {
    this.loadInitialData();
  }

  loadInitialData = async () => {
    try {
      await this.loadPeople();
      await this.loadStatistics();

      await this.loadAllTasks();
    } catch (error) {
      console.error('Error loading initial data:', error);
      this.showError('Error loading initial data');
    }
  }

  loadAllTasks = async () => {
    try {
      this.showLoading('tareas-container');
      const status = document.getElementById('estado-filter').value;
      this.tasks = await tasksAPI.getAllTasks(status);
      this.renderTasks(this.tasks);
    } catch (error) {
      console.error('Error loading tasks:', error);
      this.showError('Error loading tasks');
      document.getElementById('tareas-container').innerHTML = '<p>Could not load tasks</p>';
    }
  }

  applyLocalFilters = () => {
    const personId = document.getElementById('persona-filter').value;
    const status = document.getElementById('estado-filter').value;

    let filteredTasks = this.tasks;

    if (personId) {
      filteredTasks = filteredTasks.filter(task => task.person_id == personId);
    }

    if (status) {
      const isCompleted = status === 'completada';
      filteredTasks = filteredTasks.filter(task => task.completada === isCompleted);
    }

    this.renderTasks(filteredTasks);
  }

  loadTasks = async () => {
    const personId = document.getElementById('persona-filter').value;
    const status = document.getElementById('estado-filter').value;

    try {
      if (personId) {
        this.showLoading('tareas-container');
        const data = await tasksAPI.getTasksByPerson(personId, status);

        const personTasks = data.tareas_asignadas || [];
        this.tasks = personTasks.map(task => ({
          ...task,
          person_name: `${data.persona.nombre} ${data.persona.apellido}`,
          person_id: data.persona.id
        }));
        this.renderTasks(this.tasks);
      } else {
        await this.loadAllTasks();
        return;
      }

      if (!personId) {
        this.applyLocalFilters();
      }
    } catch (error) {
      console.error('Error loading tasks:', error);
      this.showError('Error loading tasks');
      document.getElementById('tareas-container').innerHTML = '<p>Could not load tasks</p>';
    }
  }


  loadStatistics = async () => {
    try {
      const stats = await tasksAPI.getStatistics();
      this.renderStatistics(stats);
    } catch (error) {
      console.error('Error loading statistics:', error);
      document.getElementById('stats').innerHTML = '<div class="error">Error loading statistics</div>';
    }
  }

  renderStatistics = (stats) => {
    document.getElementById('stats').innerHTML = `
            <div class="stat-card">
                <div class="stat-number">${stats.total_tareas}</div>
                <div>Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${stats.tareas_completadas}</div>
                <div>Completados</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${stats.tareas_pendientes}</div>
                <div>Pendientes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${stats.porcentaje_completado}%</div>
                <div>% Completados</div>
            </div>
        `;
  }

  loadPeople = async () => {
    try {
      const people = await tasksAPI.getPeople();
      this.people = people.results || people;
      this.renderPeopleFilter();
    } catch (error) {
      console.error('Error loading people:', error);
      this.showError('Error loading people');
    }
  }

  renderPeopleFilter = () => {
    const select = document.getElementById('persona-filter');

    while (select.children.length > 1) {
      select.removeChild(select.lastChild);
    }

    this.people.forEach((person, index) => {
      const option = document.createElement('option');
      option.value = person.id;
      option.textContent = `${person.nombre} ${person.apellido}`;
      select.appendChild(option);
    });
  }

  resetFilters = () => {
    document.getElementById('persona-filter').value = '';
    document.getElementById('estado-filter').value = '';
    this.loadAllTasks();
  }

  renderTasks = (tasks) => {
    const container = document.getElementById('tareas-container');

    if (tasks.length === 0) {
      container.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 40px;">No se encontro tareas...</p>';
      return;
    }

    container.innerHTML = tasks.map(task => this.renderTaskItem(task)).join('');
  }

  renderTaskItem = (task) => {
    const statusClass = task.completada ? 'completada' : 'pendiente';
    const statusText = task.completada ? 'Completed' : 'Pending';
    const statusIcon = task.completada ? '✅' : '⏳';

    return `
            <div class="tarea-item ${statusClass}">
                <div class="tarea-header">
                    <div class="tarea-title">${statusIcon} ${task.tarea.titulo}</div>
                    <div class="tarea-meta">
                        <span>👤 ${task.person_name}</span>
                        <span>📁 ${task.tarea.tipo_tarea}</span>
                    </div>
                </div>
                <div class="tarea-meta" style="margin-bottom: 10px;">${task.tarea.descripcion}</div>
                <div class="tarea-meta">
                    <span>📅 Start: ${this.formatDate(task.tarea.fecha_inicio)}</span> | 
                    <span>🎯 End: ${this.formatDate(task.tarea.fecha_fin)}</span> | 
                    <span><strong>Status:</strong> ${statusText}</span>
                </div>
            </div>
        `;
  }

  formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  showLoading = (containerId) => {
    document.getElementById(containerId).innerHTML = '<div class="loading">Loading...</div>';
  }

  showError = (message) => {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    setTimeout(() => {
      errorDiv.style.display = 'none';
    }, 5000);
  }
}

let tasksUI;

const resetFilters = () => {
  if (tasksUI) {
    tasksUI.resetFilters();
  }
}

document.addEventListener('DOMContentLoaded', function () {
  tasksUI = new TasksUI();
});

const loadTasks = () => {
  if (tasksUI) {
    tasksUI.loadTasks();
  }
}
