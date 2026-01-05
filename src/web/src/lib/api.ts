export interface Photo {
	id: number;
	filename: string;
	original_url: string;
	thumbnail_url: string;
	file_size: number;
	created_at: string;
}

export interface PhotoListResponse {
	photos: Photo[];
	total: number;
}

const API_BASE_URL =
	import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function fetchPhotos(): Promise<PhotoListResponse> {
	const response = await fetch(`${API_BASE_URL}/photos`);

	if (!response.ok) {
		throw new Error(`Failed to fetch photos: ${response.statusText}`);
	}

	return response.json();
}

export async function uploadPhoto(file: File): Promise<Photo> {
	const formData = new FormData();
	formData.append("file", file);

	const response = await fetch(`${API_BASE_URL}/photos`, {
		method: "POST",
		body: formData,
	});

	if (!response.ok) {
		const error = await response
			.json()
			.catch(() => ({ detail: response.statusText }));
		throw new Error(error.detail || "Failed to upload photo");
	}

	return response.json();
}

export async function deletePhoto(photoId: number): Promise<void> {
	const response = await fetch(`${API_BASE_URL}/photos/${photoId}`, {
		method: "DELETE",
	});

	if (!response.ok) {
		const error = await response
			.json()
			.catch(() => ({ detail: response.statusText }));
		throw new Error(error.detail || "Failed to delete photo");
	}
}

export function formatFileSize(bytes: number): string {
	if (bytes === 0) return "0 Bytes";

	const k = 1024;
	const sizes = ["Bytes", "KB", "MB", "GB"];
	const i = Math.floor(Math.log(bytes) / Math.log(k));

	return `${Math.round((bytes / Math.pow(k, i)) * 100) / 100} ${sizes[i]}`;
}

export function formatDate(dateString: string): string {
	const date = new Date(dateString);
	return new Intl.DateTimeFormat("en-US", {
		year: "numeric",
		month: "short",
		day: "numeric",
		hour: "2-digit",
		minute: "2-digit",
	}).format(date);
}
