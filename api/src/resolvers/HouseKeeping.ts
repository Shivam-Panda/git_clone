import { Mutation, Resolver } from "type-graphql";
import { File } from "../entity/File";
import { Folder } from "../entity/Folder";
import { Issue } from "../entity/Issue";
import { Project } from "../entity/Project";
import { Todo } from "../entity/ToDo";
import { User } from "../entity/User";

@Resolver()
export class HouseKeepingResolver {
    @Mutation(() => Boolean) 
    async hardReset() {
        await File.delete({});
        await Folder.delete({});
        await Issue.delete({});
        await Project.delete({});
        await Todo.delete({});
        await User.delete({});
    } 
}