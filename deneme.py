#%%
import os, rules, entities
basedir = 'sprites\\states'
iconlist = os.listdir(basedir)  # returns list
for icon in iconlist:
    statename= ''.join(icon.split('.')[0:-1])
    state = getattr(entities.State,statename)
    self.statespritelists[state].append(pygame.image.load(basedir+'\\'+icon))

#%%
sample

#%%
