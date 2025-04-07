def test_plot_cube(cube_center = [10.0,10.0,10.0], cube_width = 0.5):
    cw = cube_width
    cx = cube_center[0]
    cy = cube_center[1]
    cz = cube_center[2]
    points = np.array([ [cx-cw, cy-cw, cz-cw],
                        [cx+cw, cy-cw, cz-cw],
                        [cx+cw, cy+cw, cz-cw],
                        [cx-cw, cy+cw, cz-cw],
                        [cx-cw, cy-cw, cz+cw],
                        [cx+cw, cy-cw, cz+cw],
                        [cx+cw, cy+cw, cz+cw],
                        [cx-cw, cy+cw, cz+cw]])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r = [-cw,cw]
    X, Y = np.meshgrid(r, r)
    ax.plot_surface(X+cx,Y                +cy,np.array([[+cw]])+cz, alpha=0.5)
    ax.plot_surface(X+cx,Y                +cy,np.array([[-cw]])+cz, alpha=0.5)
    ax.plot_surface(X+cx,np.array([[-cw]])+cy,Y                +cz, alpha=0.5)
    ax.plot_surface(X+cx,np.array([[+cw]])+cy,Y                +cz, alpha=0.5)
    ax.plot_surface(np.array([[+cw]])+cx,X+cy,Y+cz, alpha=0.5)
    ax.plot_surface(np.array([[-cw]])+cx,X+cy,Y+cz, alpha=0.5)
    ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
