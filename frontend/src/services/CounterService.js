import ApiService from "./ApiService.js";

/**
 * Counter Service class for managing counter operations
 */
class CounterService extends ApiService {
  constructor() {
    super();
    this.basePath = "/api/counters";
  }

  /**
   * Get all counters
   * @returns {Promise<Array>}
   */
  async fetchCounters() {
    return this.get(this.basePath);
  }

  /**
   * Get a specific counter by name
   * @param {string} name
   * @returns {Promise<object>}
   */
  async getCounter(name) {
    return this.get(`${this.basePath}/${name}`);
  }

  /**
   * Create a new counter
   * @param {string} name
   * @param {number} initial_value
   * @returns {Promise<object>}
   */
  async createCounter(name, initial_value = 0) {
    return this.post(this.basePath, { name, initial_value });
  }

  /**
   * Increment a counter
   * @param {string} name
   * @param {number} amount
   * @returns {Promise<object>}
   */
  async incrementCounter(name, amount = 1) {
    return this.post(`${this.basePath}/${name}/increment`, { amount });
  }

  /**
   * Decrement a counter
   * @param {string} name
   * @param {number} amount
   * @returns {Promise<object>}
   */
  async decrementCounter(name, amount = 1) {
    return this.post(`${this.basePath}/${name}/decrement`, { amount });
  }

  /**
   * Reset a counter to 0
   * @param {string} name
   * @returns {Promise<object>}
   */
  async resetCounter(name) {
    return this.post(`${this.basePath}/${name}/reset`);
  }

  /**
   * Update a counter's value directly
   * @param {string} name
   * @param {number} value
   * @returns {Promise<object>}
   */
  async updateCounter(name, value) {
    return this.put(`${this.basePath}/${name}`, { value: parseInt(value) });
  }

  /**
   * Delete a counter
   * @param {string} name
   * @returns {Promise<object>}
   */
  async deleteCounter(name) {
    return this.delete(`${this.basePath}/${name}`);
  }
}

export default CounterService;
