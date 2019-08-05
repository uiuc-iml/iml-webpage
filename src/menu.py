import sys
import os

names = {'realtime':'Adaptive Time Stepping',
	'cooperativemotion':'Cooperative Motion Planning',
	'decisionsupport':'Clinical Decision Support',
	'drc':'DARPA Robotics Challenge',
	'dynamics':'Kinodynamic Planning',
	'slikmc':'SLIKMC',
	'vehicles':'Intelligent Vehicles',
	'knowledge':'Knowledge and Structure',
	'iv2013':'Moving Obstacles',
	'pvtp':'Optimal Acceleration-Bounded',
	'sketchmimicking':'Sketch Mimicking',
	'benchmark':'Optimal Planner Benchmarking',
	'taskandmotion':'TAMP',
	'throwing':'Throwing',
	'klampt':"Klamp't",
        'nursing':"Tele-Nursing Robot",
	'mintos':"Mintos",
	'lmpl':'LMPL',
	'parabolic':'Parabolic Path Smoother'
}
files = dict((name,name+'/index.html') for name in names.keys())
files['research']='research.html'
files['software']='software.html'
files['lmpl']='software.html#LMPL'
files['parabolic']='software.html#ParabolicSmoother'
klampt_tutorial_files = ["tutorial_install.html","tutorial_simulation.html","tutorial_math.html","tutorial_trajectory_keyframes.html",
                         "tutorial_custom_controller.html","tutorial_import_robot.html","tutorial_ik.html","tutorial_grasp.html"]
klampt_tutorial_keys = ['klampt_tutorial_'+str(i) for i in range(len(klampt_tutorial_files))]
for i,(k,v) in enumerate(zip(klampt_tutorial_keys,klampt_tutorial_files)):
    files[k]='klampt/'+v
    names[k]="Tutorial "+str(i+1)
file_to_name = dict((v,k) for (k,v) in files.items())

research_submenu = ['nursing','cooperativemotion','decisionsupport','drc','knowledge','slikmc','dynamics','vehicles','taskandmotion']
dynamics_submenu = ['realtime','sketchmimicking','throwing','mintos']
vehicles_submenu = ['iv2013','pvtp']
software_submenu = ['mintos','klampt','slikmc','iv2013']
submenus = [('research',research_submenu),
            ('dynamics',dynamics_submenu),
            ('vehicles',vehicles_submenu),
            ('software',software_submenu),
            ('klampt',klampt_tutorial_keys)]

is_absolute = os.path.dirname(sys.argv[-1])==""
relative_prefix = '' if is_absolute else '../'

def makemenuitem(link,title):
    if link==sys.argv[-1]:
        return '<a class="curmainmenu" href="%s">%s</a>' % (relative_prefix+link,title)
    else:
        return '<a href="%s">%s</a>' % (relative_prefix+link,title)

def makemenu():
    res='<ul id="mainmenu">\n'
    menufiles = [('Home','home.html'),
                 ('People','people.html'),
                 ('Research','research.html'),
                 ('Publications','publications.html'),
                 ('Software','software.html'),
                 ('Contact','contact.html')]
                 
    for (k,v) in menufiles:
        res += '<li>'+makemenuitem(v,k)+'</li>\n'
    res += '</ul>'
    return res

def makesubmenu(name,items,depth=0):
	res = '<ul class="submenu%d">\n'%(depth+1,)
	for item in items:
		if item==name:
			res += '<li class="cursubmenu">'
		else:
			res += '<li>'
		res += '<a href="%s%s">%s</a>'%(relative_prefix,files[item],names[item])
		res += '</li>\n'
        res += '</ul>\n'
	return res

def makesubmenu_recurse(name,menuname,depth=0):
	res = ''
	for (uppermenuname,uppermenuitems) in submenus:
		if menuname in uppermenuitems:
			res += makesubmenu_recurse(menuname,uppermenuname,depth+1)
                        break
        found = False
        for submenu in submenus:
            if menuname == submenu[0]:
                res += makesubmenu(name,submenu[1],depth)
                found = True
                break
        assert found
	return res

def makesubmenus():
	tgt = sys.argv[-1]
	if tgt not in file_to_name:
                print "Warning: target",tgt,"doesn't have a menu"
		return ''
	name = file_to_name[tgt]
	res = ''
	for (menuname,menuitems) in submenus:
		if name in menuitems:
			res += makesubmenu_recurse(name,menuname)
                        break
	return res


if __name__=='__main__':
    #test the makesubmenus function
    print makesubmenus()
