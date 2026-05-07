import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private BASE_URL = 'http://127.0.0.1:8001';

  constructor(private http: HttpClient) {}

  getDocuments() {
    return this.http.get<any[]>(`${this.BASE_URL}/documents`);
  }

  lockFolder(folderPath: string) {
    const formData = new FormData();
    formData.append('folder_path', folderPath);
    return this.http.post(`${this.BASE_URL}/lock-folder`, formData);
  }

  unlockFolder(folderPath: string) {
    const formData = new FormData();
    formData.append('folder_path', folderPath);
    return this.http.post(`${this.BASE_URL}/unlock-folder`, formData);
  }
}

