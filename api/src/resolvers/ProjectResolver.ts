import { Arg, Field, InputType, Int, Mutation, Query, Resolver } from "type-graphql";
import { Project } from "../entity/Project";
import { User } from "../entity/User";

@InputType()
class DeleteProjectInput {
    @Field(() => Int)
    id?: number;

    @Field(() => String)
    name?: string;

    @Field(() => String)
    owner?: string;
}

@InputType()
class FindProjectInput {
    @Field(() => Int)
    id?: number;

    @Field(() => String)
    name?: string;

    @Field(() => String)
    owner?: string;
}

@InputType()
class CreateProjectInput {
    @Field(() => String)
    key: string
    
    @Field(() => String)
    name: string;
}

@Resolver()
export class ProjectResolver {
    @Query(() => [Project]!, {nullable: true})
    async allProjects() {
        return Project.find();
    }

    @Query(() => Project!, {nullable: true})
    async findProject(@Arg("input") input: FindProjectInput) {
        if(input.id) {
            return await Project.findOne({
                where: {
                    id: input.id
                }
            })
        } else {
            return await Project.findOne({
                where: {
                    name: input.name,
                    owner: input.owner
                }
            })
        }
    }

    @Mutation(() => Int!, {nullable: true})
    async createProject(@Arg("input") input: CreateProjectInput) {
        const user = await User.findOne({
            where: {
                key: input.key
            }
        });
        if(user) {
            const projects_made = await Project.find({
                where: {
                    name: input.name,
                    owner: user.username
                }
            })
            if(projects_made.length > 0) {
                return null;
            }
            const project = await Project.create({
                name: input.name,
                issues: [],
                folders: [],
                files: [],
                owner: user.username
            }).save()
            if(project) {
                const user_projects = user.projects;
                user_projects.push(project.id);
                await User.update({
                    id: user.id
                }, {
                    projects: user_projects
                });
                return project.id;
            } else {
                return null;
            }
        } else {
            return null;
        }
    }

    @Mutation(() => Boolean)
    async deleteProject(@Arg("input") input: DeleteProjectInput) {
        if(input.id) {
            await Project.delete({
                id:input.id
            })
        } else {
            await Project.delete({
                name: input.name,
                owner: input.owner
            });
        };
        return true;
    }
}