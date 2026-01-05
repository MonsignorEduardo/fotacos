import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { AlertCircle, CheckCircle, Loader2, Upload } from "lucide-react";
import { useRef, useState } from "react";
import { PhotosTable } from "../components/PhotosTable";
import { Button } from "../components/ui/button";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "../components/ui/card";
import { fetchPhotos } from "../lib/api";
import { useDeletePhoto, useUploadPhoto } from "../lib/hooks";

const photosQueryOptions = queryOptions({
	queryKey: ["photos"],
	queryFn: fetchPhotos,
});

export const Route = createFileRoute("/")({
	loader: ({ context }) =>
		context.queryClient.ensureQueryData(photosQueryOptions),
	component: PhotoGallery,
});

function PhotoGallery() {
	const fileInputRef = useRef<HTMLInputElement>(null);
	const [uploadError, setUploadError] = useState<string | null>(null);

	const { data } = useSuspenseQuery(photosQueryOptions);

	const uploadMutation = useUploadPhoto();

	const deleteMutation = useDeletePhoto();

	const handleFileSelect = async (
		event: React.ChangeEvent<HTMLInputElement>,
	) => {
		const file = event.target.files?.[0];
		if (!file) return;

		setUploadError(null);

		try {
			await uploadMutation.mutateAsync(file);
			if (fileInputRef.current) {
				fileInputRef.current.value = "";
			}
		} catch (err) {
			setUploadError(
				err instanceof Error ? err.message : "Error al subir la foto",
			);
		}
	};

	const handleUploadClick = () => {
		fileInputRef.current?.click();
	};

	const handleDelete = async (photoId: number) => {
		if (!confirm("¿Estás seguro de que quieres eliminar esta foto?")) return;

		try {
			await deleteMutation.mutateAsync(photoId);
		} catch (err) {
			alert(err instanceof Error ? err.message : "Error al eliminar la foto");
		}
	};

	return (
		<div className="container mx-auto py-8 px-4">
			<Card>
				<CardHeader>
					<div className="flex items-center justify-between">
						<div>
							<CardTitle>Galería de Fotos</CardTitle>
							<CardDescription>Gestiona tu colección de fotos</CardDescription>
						</div>
						<div className="flex gap-2">
							<Button
								onClick={handleUploadClick}
								disabled={uploadMutation.isPending}
							>
								{uploadMutation.isPending ? (
									<>
										<Loader2 className="h-4 w-4 animate-spin" />
										Uploading...
									</>
								) : (
									<>
										<Upload className="h-4 w-4" />
										Upload Photo
									</>
								)}
							</Button>
							<input
								ref={fileInputRef}
								type="file"
								accept="image/*"
								onChange={handleFileSelect}
								className="hidden"
							/>
						</div>
					</div>
					{uploadError && (
						<div className="mt-4 flex items-center gap-2 text-sm text-red-600 bg-red-50 p-3 rounded-md">
							<AlertCircle className="h-4 w-4" />
							{uploadError}
						</div>
					)}
					{uploadMutation.isSuccess && (
						<div className="mt-4 flex items-center gap-2 text-sm text-green-600 bg-green-50 p-3 rounded-md">
							<CheckCircle className="h-4 w-4" />
							¡Foto subida exitosamente!
						</div>
					)}
				</CardHeader>
				<CardContent>
					<div className="space-y-4">
						<div className="text-sm text-slate-500">
							Total de fotos: {data?.total ?? 0}
						</div>
						<PhotosTable
							photos={data?.photos ?? []}
							onDelete={handleDelete}
							isDeleting={deleteMutation.isPending}
						/>
					</div>
				</CardContent>
			</Card>
		</div>
	);
}
