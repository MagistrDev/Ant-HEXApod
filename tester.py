import movement as mv

planes = mv.getPlanes()
hexapod = mv.Hexapod()
hexapod.move(0, 0, 0.1, planes)