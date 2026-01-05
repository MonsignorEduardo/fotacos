import {
	type ColumnDef,
	flexRender,
	getCoreRowModel,
	getSortedRowModel,
	type SortingState,
	useReactTable,
} from "@tanstack/react-table";
import { Trash2 } from "lucide-react";
import { useState } from "react";
import { formatDate, formatFileSize, type Photo } from "../lib/api";
import { Button } from "./ui/button";
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "./ui/table";

interface PhotosTableProps {
	photos: Photo[];
	onDelete: (photoId: number) => void;
	isDeleting?: boolean;
}

export function PhotosTable({
	photos,
	onDelete,
	isDeleting,
}: PhotosTableProps) {
	const [sorting, setSorting] = useState<SortingState>([]);

	const columns: ColumnDef<Photo>[] = [
		{
			accessorKey: "thumbnail_url",
			header: "Vista previa",
			cell: ({ row }) => {
				const photo = row.original;
				return (
					<div className="w-20 h-20">
						<img
							src={photo.thumbnail_url}
							alt={photo.thumbnail_url}
							className="w-full h-full object-cover rounded-md"
							loading="lazy"
						/>
					</div>
				);
			},
			enableSorting: false,
		},
		{
			accessorKey: "filename",
			header: "Nombre de archivo",
			cell: ({ row }) => {
				return (
					<div className="max-w-md">
						<div className="font-medium truncate">{row.original.filename}</div>
					</div>
				);
			},
		},
		{
			accessorKey: "file_size",
			header: "Tamaño",
			cell: ({ row }) => formatFileSize(row.original.file_size),
		},
		{
			accessorKey: "created_at",
			header: "Subida",
			cell: ({ row }) => formatDate(row.original.created_at),
		},
		{
			id: "actions",
			header: "Acciones",
			cell: ({ row }) => {
				const photo = row.original;
				return (
					<div className="flex gap-2">
						<Button
							variant="outline"
							size="sm"
							onClick={() => window.open(photo.original_url, "_blank")}
						>
							Ver
						</Button>
						<Button
							variant="destructive"
							size="sm"
							onClick={() => onDelete(photo.id)}
							disabled={isDeleting}
						>
							<Trash2 className="h-4 w-4" />
						</Button>
					</div>
				);
			},
			enableSorting: false,
		},
	];

	const table = useReactTable({
		data: photos,
		columns,
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		onSortingChange: setSorting,
		state: {
			sorting,
		},
	});

	return (
		<div className="rounded-md border">
			<Table>
				<TableHeader>
					{table.getHeaderGroups().map((headerGroup) => (
						<TableRow key={headerGroup.id}>
							{headerGroup.headers.map((header) => (
								<TableHead key={header.id}>
									{header.isPlaceholder
										? null
										: flexRender(
												header.column.columnDef.header,
												header.getContext(),
											)}
								</TableHead>
							))}
						</TableRow>
					))}
				</TableHeader>
				<TableBody>
					{table.getRowModel().rows?.length ? (
						table.getRowModel().rows.map((row) => (
							<TableRow key={row.id}>
								{row.getVisibleCells().map((cell) => (
									<TableCell key={cell.id}>
										{flexRender(cell.column.columnDef.cell, cell.getContext())}
									</TableCell>
								))}
							</TableRow>
						))
					) : (
						<TableRow>
							<TableCell colSpan={columns.length} className="h-24 text-center">
								Aún no hay fotos. ¡Sube tu primera foto!
							</TableCell>
						</TableRow>
					)}
				</TableBody>
			</Table>
		</div>
	);
}
