import { Entity, Column, PrimaryGeneratedColumn } from "typeorm";

@Entity("roles")
export class Role {
  @PrimaryGeneratedColumn("uuid", { name: "role_id" })
  user_id: string;

  @Column({ name: "name", type: "varchar", length: 255 })
  name: string;

  @Column({
    name: "created_at",
    type: "datetime",
    default: () => "CURRENT_TIMESTAMP",
  })
  createdAt: Date;
}
