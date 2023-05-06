export const environment = {
    production: false,
    baseUrl: 'http://localhost:8000/api'  
  };

export enum ApiPaths {
    Auth = '/token/',
    Refresh = '/token/refresh/',
    Register = '/users/'
 }