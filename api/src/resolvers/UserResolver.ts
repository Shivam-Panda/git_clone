import { createHash } from 'crypto';
import { Arg, Field, InputType, Int, Mutation, Query, Resolver } from "type-graphql";
import { User } from "../entity/User";

@InputType()
class CreateUserInput {
    @Field(() => String)
    username: string

    @Field(() => String)
    password: string;
}

@InputType()
class LoginInput {
    @Field(() => String)
    username: string;

    @Field(() => String)
    password: string;
}

@InputType()
class FindUserInput {
    @Field(() => Int, {nullable: true})
    id?: number

    @Field(() => String, {nullable: true})
    username?: string
}

@Resolver()
export class UserResolver {
    @Query(() => [User]) 
    async getAllUsers() {
        return await User.find();
    }

    @Mutation(() => String)
    async createUser(@Arg("input", () => CreateUserInput) input: CreateUserInput) {
        const key = createHash(input.password).digest('hex');
        const user = await User.create({
            key,
            username: input.username,
            projects: []
        }).save();
        return user.key;
    }

    @Query(() => String!, {nullable: true})
    async login(@Arg("input") input: LoginInput) {
        const key = createHash(input.password).digest('hex');
        const user = await User.findOne({
            where: {
                key,
                username: input.username
            }
        });
        if(user) {
            return user.key
        } else {
            return null;
        }
    }

    @Query(() => User!, { nullable: true })
    async findUser(@Arg("input") input: FindUserInput) {
        if(input.id) {
            const user = await User.findOne({
                where: {
                    id: input.id
                }
            })
            return user;
        } else {
            const user = await User.findOne({
                where: {
                    username: input.username
                }
            });
            return user;
        }
    }
}