import { Field, Int, ObjectType } from "type-graphql";
import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from "typeorm";

@ObjectType()
@Entity()
export class Commit extends BaseEntity {
    @Field(() => Int)
    @PrimaryGeneratedColumn()
    id: number;

    @Field(() => [Int])
    @Column("simple-array")
    files: number[]

    @Field(() => [Int])
    @Column("simple-array")
    folders: number[]

    @Field(() => String, { nullable: true })
    @Column({ nullable: true })
    name: string;

    @Field(() => Int, { nullable: true })
    @Column("int", { nullable: true })
    projectId: number;
}