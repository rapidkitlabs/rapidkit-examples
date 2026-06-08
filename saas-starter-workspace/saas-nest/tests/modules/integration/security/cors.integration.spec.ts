import { Test, TestingModule } from "@nestjs/testing";

import { CorsController } from "../../../../src/modules/free/security/cors/cors.controller";
import { CorsHealthController } from "../../../../src/health/cors.health";
import { CorsService } from "../../../../src/modules/free/security/cors/cors.service";

describe("Cors Module Integration", () => {
  let controller: CorsController;
  let healthController: CorsHealthController;
  let service: CorsService;

  beforeAll(async () => {
    const moduleRef: TestingModule = await Test.createTestingModule({
      controllers: [
        CorsController,
        CorsHealthController,
      ],
      providers: [CorsService],
    }).compile();

    controller = moduleRef.get(CorsController);
    healthController = moduleRef.get(CorsHealthController);
    service = moduleRef.get(CorsService);
  });

  it("should expose metadata with enabled policy", () => {
    const metadata = controller.getMetadata();

    expect(metadata).toBeDefined();
    expect(metadata.module).toBe("cors");
    expect(metadata.enabled).toBe(true);
    expect(metadata.policy.allow_origins.length).toBeGreaterThan(0);
    expect(metadata.log_level).toBe("INFO");
    expect(metadata.metadata).toEqual({});
    expect(metadata.features).toContain("cors_middleware");
  });

  it("should report feature catalogue", () => {
    const payload = controller.listFeatures();

    expect(payload.features).toContain("cors_middleware");
    expect(payload.features).toContain("http_security_headers");
  });

  it("should surface health payload through both controllers", () => {
    const metadata = controller.getMetadata();
    const dedicatedHealth = healthController.getModuleHealth();

    expect(metadata.enabled).toBe(true);
    expect(dedicatedHealth.status).toBe("ok");
    expect(metadata.policy.allow_origins).toBeDefined();
    expect(Array.isArray(dedicatedHealth.features)).toBe(true);
  });

  it("should allow service overrides", () => {
    service.setCorsOptions({ origin: ["https://example.com"] });

    const metadata = controller.getMetadata();

    expect(metadata.policy.allow_origins).toContain("https://example.com");
  });
});
