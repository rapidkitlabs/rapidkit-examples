import { Test, TestingModule } from '@nestjs/testing';

import { AppController } from '../src/app.controller';
import { AppService } from '../src/app.service';
import { SupportAgentService } from '../src/agents/support-agent.service';

describe('AppController', () => {
  let appController: AppController;

  beforeEach(async () => {
    const app: TestingModule = await Test.createTestingModule({
      controllers: [AppController],
      providers: [
        AppService,
        {
          provide: SupportAgentService,
          useValue: {
            handleTicket: async () => ({
              ai_response: 'ok',
              latency_ms: 0,
              next_action: 'monitor',
              provider: 'test',
              ticket_id: 'TKT-TEST',
              urgency: 'low',
            }),
          },
        },
      ],
    }).compile();

    appController = app.get<AppController>(AppController);
  });

  it('should return health status', () => {
    const result = appController.getHealth();
    expect(result).toHaveProperty('status', 'ok');
  });

  // <<<inject:controller-tests>>>
});
