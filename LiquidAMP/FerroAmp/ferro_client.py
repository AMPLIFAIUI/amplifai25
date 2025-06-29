import asyncio
import websockets
import json
import pygame
import sys
import random
import numpy as np
from pygame import gfxdraw

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FerroChat - Fluid Chat Client")
clock = pygame.time.Clock()

# Ferrofluid simulation
PARTICLE_COUNT = 800
particles = np.zeros((PARTICLE_COUNT, 5))  # x, y, vx, vy, size

class FerroClient:
    def __init__(self):
        self.uri = "ws://localhost:8765"
        self.websocket = None
        self.messages = []
        self.input_text = ""
        self.font = pygame.font.SysFont('Arial', 18)
        self.init_particles()
        self.connection_status = "Connecting..."
        
    def init_particles(self):
        global particles
        particles = np.array([
            [random.randint(0, WIDTH), random.randint(0, HEIGHT),
             random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(2, 4)]
            for _ in range(PARTICLE_COUNT)
        ])

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connection_status = "Connected!"
            asyncio.create_task(self.receive_messages())
        except Exception as e:
            self.connection_status = f"Connection failed: {str(e)}"

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                self.messages.append(data)
                self.apply_message_effect(data['content'])
        except websockets.exceptions.ConnectionClosed:
            self.connection_status = "Disconnected from server"

    async def send_message(self, message):
        if self.websocket and message.strip():
            await self.websocket.send(message)
            self.input_text = ""

    def apply_message_effect(self, message):
        intensity = min(len(message) / 15, 3.0)
        center_x, center_y = WIDTH//2, HEIGHT//2
        
        for i in range(PARTICLE_COUNT):
            # Create magnetic field effect
            dx = particles[i, 0] - center_x
            dy = particles[i, 1] - center_y
            dist = max(1, (dx**2 + dy**2)**0.5)
            
            force = intensity * 50 / dist
            angle = np.arctan2(dy, dx)
            
            particles[i, 2] += -np.cos(angle) * force
            particles[i, 3] += -np.sin(angle) * force

    def update_particles(self):
        particles[:, 0] += particles[:, 2]
        particles[:, 1] += particles[:, 3]
        
        # Boundary checks with bounce
        mask_x = (particles[:, 0] < 0) | (particles[:, 0] > WIDTH)
        mask_y = (particles[:, 1] < 0) | (particles[:, 1] > HEIGHT)
        particles[:, 2][mask_x] *= -0.8
        particles[:, 3][mask_y] *= -0.8
        
        # Random movement and friction
        particles[:, 2] = particles[:, 2] * 0.98 + np.random.normal(0, 0.05, PARTICLE_COUNT)
        particles[:, 3] = particles[:, 3] * 0.98 + np.random.normal(0, 0.05, PARTICLE_COUNT)

    def draw(self):
        screen.fill((10, 10, 30))  # Dark background
        
        # Draw particles with gradient
        for x, y, _, _, size in particles:
            dist_to_center = ((x-WIDTH/2)**2 + (y-HEIGHT/2)**2)**0.5
            blue = min(255, 150 + dist_to_center/2)
            alpha = min(255, 100 + size*20)
            color = (100, 150, blue, alpha)
            pygame.gfxdraw.filled_circle(screen, int(x), int(y), int(size), color)
            pygame.gfxdraw.aacircle(screen, int(x), int(y), int(size), color)
        
        # Draw chat UI
        pygame.draw.rect(screen, (20, 20, 50), (0, HEIGHT-120, WIDTH, 120))
        
        # Display messages
        for i, msg in enumerate(self.messages[-6:]):
            text = self.font.render(
                f"{msg['timestamp'][11:19]} - {msg['content']}", 
                True, (220, 220, 255))
            screen.blit(text, (20, HEIGHT - 160 - i * 25))
        
        # Input box
        pygame.draw.rect(screen, (40, 40, 80), (20, HEIGHT-70, WIDTH-40, 40))
        input_surface = self.font.render(self.input_text, True, (255, 255, 255))
        screen.blit(input_surface, (30, HEIGHT-60))
        
        # Connection status
        status_surface = self.font.render(self.connection_status, True, (255, 255, 0))
        screen.blit(status_surface, (20, 20))

async def main_loop(client):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    await client.send_message(client.input_text)
                elif event.key == pygame.K_BACKSPACE:
                    client.input_text = client.input_text[:-1]
                else:
                    client.input_text += event.unicode
        
        client.update_particles()
        client.draw()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
    
    pygame.quit()
    sys.exit()

async def main():
    client = FerroClient()
    await client.connect()
    await main_loop(client)

if __name__ == "__main__":
    asyncio.run(main())