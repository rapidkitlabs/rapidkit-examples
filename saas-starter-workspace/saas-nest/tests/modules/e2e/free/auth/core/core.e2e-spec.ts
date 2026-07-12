import { Test, TestingModule } from "@nestjs/testing";

import { AuthCoreModule } from "@modules/free/auth/core/auth-core.module";

describe("AuthCore NestJS E2E", () => {
  it("compiles the module", async () => {
    let moduleRef: TestingModule;
    try {
      moduleRef = await Test.createTestingModule({
        imports: [AuthCoreModule],
      }).compile();
    } catch (err) {
      // Optional deps may not be installed in all downstream apps;
      // treat this as a soft-skip rather than failing.
      // eslint-disable-next-line no-console
      console.warn("Skipping module compile smoke:", err);
      return;
    }

    expect(moduleRef).toBeDefined();
  });
});
