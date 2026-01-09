import axios, { AxiosInstance, AxiosError } from 'axios';
import { apiConfig } from '../config/api.config';

export class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: apiConfig.baseURL,
      timeout: apiConfig.timeout,
      headers: apiConfig.headers,
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          const message = this.getErrorMessage(error);
          return Promise.reject(new Error(message));
        }
        return Promise.reject(error);
      }
    );
  }

  private getErrorMessage(error: AxiosError): string {
    if (error.response?.data && typeof error.response.data === 'object') {
      const data = error.response.data as { detail?: string };
      return data.detail || 'Erro na requisição';
    }
    return 'Erro ao conectar com o servidor';
  }

  get<T>(url: string, config?: any): Promise<T> {
    return this.client.get<T>(url, config).then((response) => response.data);
  }

  post<T>(url: string, data?: any, config?: any): Promise<T> {
    return this.client.post<T>(url, data, config).then((response) => response.data);
  }

  put<T>(url: string, data?: any, config?: any): Promise<T> {
    return this.client.put<T>(url, data, config).then((response) => response.data);
  }

  delete<T>(url: string, config?: any): Promise<T> {
    return this.client.delete<T>(url, config).then((response) => response.data);
  }
}

export const apiClient = new ApiClient();

