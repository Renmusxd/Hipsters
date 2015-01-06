import pygame, random, sys

def sumwithin(arr,pos,dist,filter=(lambda x:x)):
	s = 0
	checked = 0
	seen = set([])
	for y in range(pos[1]-dist,pos[1]+dist+1):
		for x in range(pos[0]-dist,pos[0]+dist+1):
			if y<0 or y>=len(arr) or x<0 or x>=len(arr[y]):
				continue
			if x==pos[0] and y==pos[1]:
				continue
			s += filter(arr[x][y])
			checked += 1
			seen.add(arr[x][y])
	return s, checked, seen

def main(check_dist, ratio_switch,options=[0,1],coloroptions={0:(255,255,255),1:(0,0,0)}):
	pygame.init()
	size = width, height = 300,300

	screen = pygame.display.set_mode(size)

	people = [[random.choice(options) for x in range(width)] for y in range(height)]
	step = 0
	while step<10:
		step+=1
		print("step "+str(step))
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		peoplecopy = [row[:] for row in people]

		total = 0
		opt_totals = {}
		for opt in options:
			opt_totals[opt] = 0

		pixels = pygame.surfarray.array3d(screen)
		
		for y in range(height):
			for x in range(width):
				me = peoplecopy[x][y]
				s, c, seen = sumwithin(people,(x,y),check_dist,(lambda x: x==me))
				if float(s)/c >= ratio_switch:
					newme = random.choice(list(seen))
					people[x][y] = newme
					pixels[x][y] = coloroptions[newme]
					opt_totals[newme] += 1
				else:
					opt_totals[me] += 1
				total +=1
		for opt in options:
			print("  "+str(opt)+": "+str(float(opt_totals[opt])/total))
		pygame.surfarray.blit_array(screen, pixels)
		pygame.display.flip()
		pygame.image.save(screen,"Step_"+str(step)+".png")