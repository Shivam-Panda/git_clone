import { File } from "src/entity/File";
import { Folder } from "src/entity/Folder";
import { Project } from "src/entity/Project";
import { Arg, Field, InputType, Int, Mutation, Query, Resolver } from "type-graphql";

@InputType()
class GetFileInput {
    @Field(() => String)
    name: string;

    @Field(() => Int)
    projectId: number;
}

@InputType()
class CreateFileInput {
    @Field(() => Int)
    projectId: number

    @Field(() => String)
    fileName: string;

    @Field(() => String)
    body: string;
}

@InputType()
class CreateFolderInput {
    @Field(() => Int)
    projectId: number

    @Field(() => String)
    folderName: string;

    @Field(() => [String])
    files: Array<string>;
}

@Resolver()
export class FileResolver {
    @Mutation(() => Boolean, { nullable: true })
    async commit(@Arg("input") input: any, @Arg("projectId") projectId: number) {
        const project = await Project.findOne({
            where: {
                id: projectId
            }
        });
        if(project) {
            const project_files = project.files;
            const project_folder = project.folders;
            const file_to_folder: any = {};
            for(const key in input) {
                if(key.includes('.')) {
                    // File
                    // Do Nothing
                } else {
                    // Folder
                    const folder_vals = input[key]
                    for(let i = 0; i < folder_vals.length; i++) {
                        if(folder_vals[i].includes('.')) {
                            const f = await File.create({
                                fileName: folder_vals[i],
                                body: input[folder_vals[i]],
                                folder: key
                            }).save()
                            project_files.push(f.id);
                        } else {
                            file_to_folder[folder_vals[i]] = key
                        }
                    }
                }
            }

            for(const key in file_to_folder) {
                const f = await Folder.create({
                    files: input[key],
                    parentFolder: file_to_folder[key],
                    name: key,
                    projectId: projectId
                }).save()
                project_folder.push(f.id);
            }
            
            await Project.update({
                id: projectId
            }, {
                files: project_files,
                folders: project_folder
            })
            return true;
        } else {
            return null;
        }
    }

    @Query(() => String, {nullable: true})
    async pullRequest(@Arg('projectId') projectId: number) {
        const project = await Project.findOne({
            where: {
                id: projectId
            }
        });
        if(project) {
            const sender: any = {};
            const proj_folders: Folder[] = [];
            const proj_files: File[] = [];
            for(let i = 0; i < project.files.length; i++) {
                const cur_file = await File.findOne({
                    where: {
                        id: project.files[i]
                    }
                });
                if(cur_file) {
                    proj_files.push(cur_file)
                }
            }
            for(let i = 0; i < project.folders.length; i++) {
                const cur_file = await Folder.findOne({
                    where: {
                        id: project.folders[i]
                    }
                });
                if(cur_file) {
                    proj_folders.push(cur_file)
                }
            }
            proj_files.forEach((file, _) => {
                sender[file.fileName] = file.body;
            });
            proj_folders.forEach((folder, _) => {
                let dir: string[] = [];
                proj_files.forEach((file, _) => {
                    if(file.folder == folder.name) {
                        dir.push(file.fileName);
                    }
                })
                proj_folders.forEach((childFolder, _) => {
                    if(childFolder.parentFolder == folder.name) {
                        dir.push(childFolder.name);
                    }
                })
                sender[folder.name] = dir;
            })
            return JSON.stringify(sender);
        } else {
            return null;
        }
    }

    @Query(() => File!, {nullable: true})
    async getFile(@Arg("input") input: GetFileInput) {
        const project = await Project.findOne({
            where: {
                id: input.projectId
            }
        }) ;
        if(project) {
            return await File.findOne({
                where: {
                    projectId: input.projectId,
                    fileName: input.name
                }
            });
        } else {
            return null;
        }
    }

    @Query(() => Array<String>, {nullable: true})
    async getFolder(@Arg("input") input: GetFileInput) {
        const project = await Project.findOne({
            where: {
                id: input.projectId
            }
        })
        if(project) {
            const files = [];
            for(let i = 0; i < project.files.length; i++) {
                const cur_file = await File.findOne({
                    where: {
                        id: project.files[i]
                    }
                });
                if(cur_file && cur_file.folder == input.name) {
                    files.push(cur_file.fileName);
                }
            }
            for(let i = 0; i < project.folders.length; i++) {
                const cur_file = await Folder.findOne({
                    where: {
                        id: project.folders[i]
                    }
                });
                if(cur_file && cur_file.parentFolder == input.name) {
                    files.push(cur_file.name);
                }
            }
            return files;
        } else {
            return null;
        }
    }
}