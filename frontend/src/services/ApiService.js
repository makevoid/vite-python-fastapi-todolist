/**
 * Base API Service class for handling HTTP requests
 */
class ApiService {
  constructor(baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000") {
    this.baseURL = baseURL;
  }

  /**
   * Make a GET request
   * @param {string} endpoint
   * @returns {Promise<any>}
   */
  async get(endpoint) {
    const response = await fetch(`${this.baseURL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`GET ${endpoint} failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Make a POST request
   * @param {string} endpoint
   * @param {object} data
   * @returns {Promise<any>}
   */
  async post(endpoint, data = null) {
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, options);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `POST ${endpoint} failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Make a PUT request
   * @param {string} endpoint
   * @param {object} data
   * @returns {Promise<any>}
   */
  async put(endpoint, data) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `PUT ${endpoint} failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Make a DELETE request
   * @param {string} endpoint
   * @returns {Promise<any>}
   */
  async delete(endpoint) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `DELETE ${endpoint} failed: ${response.statusText}`);
    }
    return response.json();
  }
}

export default ApiService;
