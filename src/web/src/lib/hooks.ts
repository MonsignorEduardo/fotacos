import {
	queryOptions,
	useMutation,
	useQueryClient,
} from "@tanstack/react-query";
import { deletePhoto, fetchPhotos, uploadPhoto } from "./api";

export const PHOTOS_QUERY_KEY = ["photos"];

export const photosQueryOptions = queryOptions({
	queryKey: PHOTOS_QUERY_KEY,
	queryFn: fetchPhotos,
});

export function useUploadPhoto() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: uploadPhoto,
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: PHOTOS_QUERY_KEY });
		},
	});
}

export function useDeletePhoto() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: deletePhoto,
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: PHOTOS_QUERY_KEY });
		},
	});
}
