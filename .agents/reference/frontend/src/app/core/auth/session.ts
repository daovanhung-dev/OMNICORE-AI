let accessToken: string | undefined;
export function setAccessToken(token: string | undefined): void { accessToken = token; }
export function getAccessToken(): string | undefined { return accessToken; }
export function clearSession(): void { accessToken = undefined; }
