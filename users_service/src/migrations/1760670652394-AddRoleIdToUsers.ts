import { MigrationInterface, QueryRunner } from "typeorm";

export class AddRoleIdToUsers1760671000001 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE users
      ADD COLUMN role_id CHAR(36) NULL
    `);

    await queryRunner.query(`
      UPDATE users
      SET role_id = (
        SELECT role_id FROM roles WHERE name = 'user'
      )
    `);

    await queryRunner.query(`
      UPDATE users
      SET role_id = (
        SELECT role_id FROM roles WHERE name = 'admin'
      )
      WHERE email = 'croman@admin.com'
    `);

    await queryRunner.query(`
      ALTER TABLE users
      ADD CONSTRAINT FK_users_roles
      FOREIGN KEY (role_id) REFERENCES roles(role_id)
      ON DELETE SET NULL ON UPDATE CASCADE
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE users DROP FOREIGN KEY FK_users_roles
    `);

    await queryRunner.query(`
      ALTER TABLE users DROP COLUMN role_id
    `);
  }
}
