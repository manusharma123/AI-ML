import { Component, OnInit } from '@angular/core';
import { ApiService } from './services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {

  folderPath = '';
  documents: any[] = [];
  message = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadDocuments();
  }

  loadDocuments() {
    this.api.getDocuments().subscribe({
      next: (data: any) => this.documents = data,
      error: () => this.message = 'Failed to load documents'
    });
  }

  lock() {
    if (!this.folderPath) return;
    this.api.lockFolder(this.folderPath).subscribe(() => {
      this.message = 'Folder locked';
    });
  }

  unlock() {
    if (!this.folderPath) return;
    this.api.unlockFolder(this.folderPath).subscribe(() => {
      this.message = 'Folder unlocked';
    });
  }

  onFolderSelect(event: any) {
    if (event.target.files.length > 0) {
      const path = event.target.files[0].webkitRelativePath;
      this.folderPath = path;
      // this.folderPath = path.split('/')[0];
    }
  }
}