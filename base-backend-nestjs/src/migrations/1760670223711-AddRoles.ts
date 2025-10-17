import { MigrationInterface, QueryRunner } from "typeorm";

export class AddRoles1760670223711 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      INSERT INTO roles (role_id, name) VALUES (UUID(), 'user');
    `);
    await queryRunner.query(`
      INSERT INTO roles (role_id, name) VALUES (UUID(), 'vendor');
    `);
    await queryRunner.query(`
      INSERT INTO roles (role_id, name) VALUES (UUID(), 'admin');
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      DELETE FROM roles WHERE name = 'user';
    `);
    await queryRunner.query(`
      DELETE FROM roles WHERE name = 'vendor';
    `);
    await queryRunner.query(`
      DELETE FROM roles WHERE name = 'admin';
    `);
  }
}
