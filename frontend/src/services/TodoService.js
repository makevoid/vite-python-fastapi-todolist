import ApiService from "./ApiService.js";

/**
 * Todo Service class for managing todo operations
 */
class TodoService extends ApiService {
  constructor() {
    super();
    this.basePath = "/api/todos";
  }

  /**
   * Get all todos
   * @returns {Promise<Array>}
   */
  async fetchTodos() {
    return this.get(this.basePath);
  }

  /**
   * Get a specific todo by ID
   * @param {number} id
   * @returns {Promise<object>}
   */
  async getTodo(id) {
    return this.get(`${this.basePath}/${id}`);
  }

  /**
   * Create a new todo
   * @param {string} title
   * @param {string} description
   * @returns {Promise<object>}
   */
  async createTodo(title, description = '') {
    return this.post(this.basePath, { title, description });
  }

  /**
   * Update a todo
   * @param {number} id
   * @param {object} updates - Object with title, description, and/or completed fields
   * @returns {Promise<object>}
   */
  async updateTodo(id, updates) {
    return this.put(`${this.basePath}/${id}`, updates);
  }

  /**
   * Toggle a todo's completion status
   * @param {number} id
   * @returns {Promise<object>}
   */
  async toggleTodoCompletion(id) {
    return this.post(`${this.basePath}/${id}/toggle`);
  }

  /**
   * Delete a todo
   * @param {number} id
   * @returns {Promise<object>}
   */
  async deleteTodo(id) {
    return this.delete(`${this.basePath}/${id}`);
  }
}

export default TodoService;
