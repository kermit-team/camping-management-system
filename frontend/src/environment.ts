export const environment = {
    production: false,
    baseUrl: 'http://localhost:8000/api'  
  };


export enum ApiPaths {
    Auth = '/token/',
    Refresh = '/token/refresh/',
    Register = '/users/',
    EmailConfirmation = '/email-verification/',
    ResetPassword = '/password-reset/',
    ConfirmResetPassword = '/password-reset/confirm/',
    GetUpdateUser = '/users/',
    GetPlots = '/camping-plots/',
    GetAvailablePlots = '/camping-plots/available/',
    CreateCar = '/cars/',
    GetAllUsers = '/users/',
    DeleteUser = '/users/',
    GetAllGroups = '/groups/',
    Reservations = '/reservations/'
 }