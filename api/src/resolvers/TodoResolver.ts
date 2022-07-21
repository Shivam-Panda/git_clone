import { Project } from "src/entity/Project";
import { Arg, Field, InputType, Int, Mutation, Query, Resolver } from "type-graphql";
import { Item } from "../entity/Item";
import { Todo } from "../entity/Todo";

@InputType()
class NewTodoInput {
    @Field(() => String)
    title: string;

    @Field(() => String)
    description: string;

    @Field(() => String)
    category: string;

    @Field(() => Int)
    todoId: number
};

@InputType()
class UpdatePositionInput {
    @Field(() => String)
    current: string;

    @Field(() => String)
    next: string;

    @Field(() => Int)
    todoId: string;

    @Field(() => Int)
    itemId: string;
}

@Resolver()
export class TodoResolver {
    @Mutation(() => Int, { nullable: true })
    async newTodo(@Arg("input") input: NewTodoInput) {
        const todo = await Todo.findOne({
            where: {
                id: input.todoId
            }
        });
        if(!todo) return null;
        const i = await Item.create({
            title: input.title,
            description: input.description,
            todoId: todo.id
        }).save()
        switch(input.category) {
            case "todo":
                const ts = todo.todo;
                ts.push(i.id);
                await Todo.update(
                {
                    id: todo.id
                },
                {
                    todo: ts
                });
                break;
            case "current":
                const curs = todo.current;
                curs.push(i.id);
                await Todo.update(
                    {
                        id: todo.id
                    },{
                        current: curs
                    }
                );
                break;
            case "done":
                const done = todo.done;
                done.push(i.id);
                await Todo.update(
                    {
                        id: todo.id
                    },
                    {
                        done
                    }
                )
                break;
        }
        return i.id;
    }

    @Query(() => [Item], { nullable: true })
    async getItems(@Arg("category") category: string, @Arg("id") id: number) {
        const todo = await Todo.findOne({
            where: {
                id
            }
        });
        if(!todo) return null;
        let t_items: number[] = [];
        switch(category) {
            case "todo":
                t_items = todo.todo;
                break;
            case "current":
                t_items = todo.current
                break;
            case "done": 
                t_items = todo.done;
                break;
        }

        const items = [];

        for(let i = 0; i < t_items.length; i++) {
            const i = await Item.findOne({
                where: {
                    id: t_items[i]
                }
            })
            if(i) {
                items.push(i)
            }
        }
        return items;
    }

    @Mutation(() => Boolean)
    async updatePosition(@Arg("input") input: UpdatePositionInput) {
        const todo = await Todo.findOne({
            where: {
                id: input.todoId
            }
        });
        const item = await Item.findOne({
            where: {
                id: input.itemId
            }
        })

        if(!todo) return false;
        if(!item) return false;
        let curs: number[] = []
        let nexts: number[] = []

        switch(input.current) {
            case "todo":
                curs = todo.todo 
                curs.filter((val,i) => {
                    if(val == item.id) {
                        return false;
                    }
                    return true;
                })
                await Todo.update({
                    id: input.id
                }, {
                    todo: curs
                });
                break;
            case "current":
                curs = todo.current 
                curs.filter((val,i) => {
                    if(val == item.id) {
                        return false;
                    }
                    return true;
                })
                await Todo.update({
                    id: input.id
                }, {
                    current: curs
                });
                break;
            case "done":
                curs = todo.done 
                curs.filter((val,i) => {
                    if(val == item.id) {
                        return false;
                    }
                    return true;
                })
                await Todo.update({
                    id: input.todoId
                }, {
                    done: curs
                });
                break;
        }

        switch(input.next) {
            case "todo":
                nexts = todo.todo
                nexts.push(item.id)
                await Todo.update({
                    id: input.todoId
                }, {
                    todo: nexts
                })
                break;
            case "current":
                nexts = todo.current
                nexts.push(item.id)
                await Todo.update({
                    id: input.todoId
                }, {
                    current: nexts
                })
                break;
            case "done":
                nexts = todo.done
                nexts.push(item.id)
                await Todo.update({
                    id: input.todoId
                }, {
                    done: nexts
                })
                break;
        }
    }

    @Mutation(() => Boolean)
    async initTodo(@Arg("id") id: number) {

    }

    @Mutation(() => Boolean)
    async deleteItem(@Arg("id") id: number) {
        const i = await Item.findOne({
            where: {
                id
            }
        });
        if(!i) return false;
        await Item.delete({
            where: {
                id
            }
        });
        return true;
    }

    @Mutation(() => Boolean)
    async deleteItem(@Arg("id") id: number, @Arg("todoId") todoId: number) {
        const i = await Item.findOne({
            where: {
                id
            }
        })
        const todo = await Todo.findOne({
            where: {
                id: todoId 
            }
        });
        if(!todo || !i) return false;
        await Item.delete({
            where: {
                id
            }
        });
        const ts = todo.todo;
        const c = todo.current;
        const d = todo.done;
        ts.filter((val) => {
            if(val == id) return false;
            return true;
        })
        c.filter((val) => {
            if(val == id) return false;
            return true;
        })
        d.filter((val) => {
            if(val == id) return false;
            return true;
        })
        await Todo.update({
            id: todoId
        }, {
            current: c,
            done: d,
            todo: ts
        });
        return true;
    }

    @Mutation(() => Boolean)
    async deleteTodo(@Arg("id") id: number, @Arg("projectId") projectId: number) {
        const t = await Todo.findOne({
            where: {
                id
            }
        });
        const p = await Project.findOne({
            where: {
                id: projectId
            }
        });
        if(!t || !p) return false;
        await Project.update({
            id: projectId
        }, {
            todo: null
        })
        await Todo.delete({
            where: {
                id
            }
        })
        
        return true;
    }
}
