"""
Test script for assetDB.
"""
import sys
import os
import random
import datetime
import getpass
from collections import defaultdict
from sqlalchemy import create_engine


path = os.path.join(os.path.dirname(__file__))
sys.path.append(path)


import assetDB.setup as setup
import assetDB.models.modelbase as base
from assetDB.models import *
import assetDB.config as config


def createGenericStatus(StatusClass,
                        names=None,
                        labels=None,
                        descriptions=None):
    if names is None:
        names = ['complete', 'in_progress', 'open']
    if labels is None:
        labels = ['Label'] * len(names)
    if descriptions is None:
        descriptions = ['Description'] * len(names)
    statuses = []
    for name, label, desc in zip(names, labels, descriptions):
        ps = StatusClass(
            name=name,
            label=label,
            description=desc
        )
        statuses.append(ps)
    return statuses


def createConfigFile(session,
                     name=None,
                     version=1, revision=1,
                     status=None,
                     category=None):
    if name is None:
        name = 'name'
    if status is None:
        statues = session.query(ConfigFileStatus).all()
        status = random.choice(statues)
    if category is None:
        categories = session.query(ConfigFileCategory).all()
        category = random.choice(categories)

    cfg = ConfigFile(
        name=name,
        config_file_status=status,
        config_file_category=category
    )

    cfgv = ConfigFileVersion(
        config_file=cfg,
        version=version,
        revision=revision,
    )
    return cfg, cfgv


def createConfigFiles(session):
    # Config File Statuses
    names = ['na', 'active', 'deprecated']
    labels = ['N/A', 'active', 'Deprecated']
    statuses = createGenericStatus(
        ConfigFileStatus,
        names=names,
        labels=labels
    )
    session.add_all(statuses)
    session.commit()

    # Config File Categories
    names = ['shot', 'project', 'base']
    labels = ['Shot Level', 'Project Level', 'Base Level']
    categories = createGenericStatus(
        ConfigFileCategory,
        names=names,
        labels=labels
    )
    session.add_all(categories)
    session.commit()

    # ConfigFile
    names = ['system', 'linux', 'windows', 'jerry']
    configFiles = []
    for name in names:
        cfg, cfgv = createConfigFile(
            session,
            name=name,
            version=random.randint(1, 10),
            revision=random.randint(1, 3),
            status=random.choice(statuses),
            category=random.choice(categories)
        )
        configFiles.append(cfg)
        configFiles.append(cfgv)
    session.add_all(configFiles)
    session.commit()
    return


def queryConfigFiles(session):
    # Query...
    q = session.query(ConfigFile)
    all_config_files = q.all()
    print '=' * 80
    print 'ConfigFile...'
    for cfile in all_config_files:
        print '-' * 25
        print 'name:', cfile.name
        print 'status:', cfile.config_file_status

    q = session.query(ConfigFileVersion)
    all_config_file_versions = q.all()
    print '=' * 80
    print 'ConfigFileVersion...'
    for cver in all_config_file_versions:
        print '-' * 25
        print 'version:', cver.version
        print 'revision:', cver.revision
        print 'file:', cver.config_file
        print 'status:', cver.config_file.config_file_status
    return


def createUsers(session):
    # Sites
    names = ['london', 'newyork', 'rome', 'vancouver']
    sites = []
    for name in names:
        cfg = config.getSiteConfig(name)
        s = Site(name=name, **cfg)
        sites.append(s)
    session.add_all(sites)
    session.commit()

    # Departments
    names = ['animation', 'production', 'modelling', 'rigging']
    labels = ['Animation', 'Production', 'Modelling', 'Rigging']
    depts = []
    for name, label in zip(names, labels):
        d = Department(name=name, label=label)
        depts.append(d)
    session.add_all(depts)
    session.commit()

    # (Parent) User Groups
    names = ['company1', 'company2']
    parent_user_groups = []
    for name in names:
        ug = UserGroup(
            name=name,
        )
        parent_user_groups.append(ug)
    session.add_all(parent_user_groups)
    session.commit()

    # User Groups
    names = ['upstairs', 'downstairs']
    user_groups = []
    for name in names:
        ug = UserGroup(
            name=name,
        )
        ug.parent = random.choice(parent_user_groups)
        user_groups.append(ug)
    session.add_all(user_groups)
    session.commit()

    # User Status
    names = ['active', 'na']
    statuses = createGenericStatus(UserStatus, names=names)
    session.add_all(statuses)
    session.commit()

    # Users
    user_name = getpass.getuser()
    names = [user_name, 'david', 'jeff', 'mark', 'robert', 'jez', 'superhans']
    users = []
    for name in names:
        u = User(
            user_name=name,
            password='password',
            first_name=name,
            last_name=name,
            email_address=name + '@domain.com',
            user_status=random.choice(statuses),
        )
        u.user_groups.append(random.choice(user_groups))
        u.department = random.choice(depts)
        u.site = random.choice(sites)
        users.append(u)
    session.add_all(users)
    session.commit()
    return


def queryUsers(session):
    # Query all Sites
    q = session.query(Site)
    all_sites = q.all()
    print '=' * 80
    print 'Sites...'
    for site in all_sites:
        print '-' * 25
        print 'name:', site.name
        print 'address:', site.address
        print 'created_user_name:', site.created_user_name
        print 'created_user:', site.created_user
        print 'site:', site.created_user

    # Query all Departments
    q = session.query(Department)
    all_departments = q.all()
    print '=' * 80
    print 'Departments...'
    for dept in all_departments:
        print '-' * 25
        print 'name:', dept.name
        print 'label:', dept.label
        print 'description:', dept.description
        print 'users:', dept.users

    # Query all UserStatuses
    q = session.query(UserStatus)
    all_user_statuss = q.all()
    print '=' * 80
    print 'UserStatuses...'
    for status in all_user_statuss:
        print '-' * 25
        print 'name:', status.name
        print 'label:', status.label
        print 'description:', status.description

    # Query all UserGroups
    q = session.query(UserGroup)
    all_user_groups = q.all()
    print '=' * 80
    print 'UserGroups...'
    for user_group in all_user_groups:
        print '-' * 25
        print 'name:', user_group.name
        print 'users:', user_group.users
        print 'children:', user_group.children
        print 'parent:', user_group.parent

    # Query all users
    q = session.query(User)
    all_users = q.all()
    # all_users = q.filter_by(user_name='jez').all()
    print '=' * 80
    print 'Users...'
    for user in all_users:
        print '-' * 25
        print 'name:', user.user_name
        print 'site:', user.site
        print 'dept:', user.department
        print 'status:', user.user_status
        print 'users:', user.user_status.users
    return


def createTasks(session):
    # Query everything
    sites = session.query(Site).all()
    users = session.query(User).all()
    depts = session.query(Department).all()
    # cur_user = assetDB.setup.get_current_user(session)

    # Task Status
    names = ['complete', 'in_progress', 'open']
    task_statuses = createGenericStatus(TaskStatus, names=names)
    session.add_all(task_statuses)
    session.commit()
    
    # Task Category
    names = ['category']
    task_categories = createGenericStatus(TaskCategory, names=names)
    session.add_all(task_categories)
    session.commit()

    # Tasks
    names = ['model', 'camera', 'animation',
             'rig', 'shader', 'texture',
             'lighting', 'render', 'effects',
             'comp']
    tasks = []
    date_ranges = []
    for name in names:
        status = random.choice(task_statuses)
        category = random.choice(task_categories)
        u = Task(
            name=name,
            task_category=category,
            task_status=status,
            # task_status_id=status.id,
        )
        u.users.append(random.choice(users))
        u.department = random.choice(depts)
        u.site = random.choice(sites)
        num_date_ranges = random.randint(1, 2)
        for i in range(num_date_ranges):
            st = datetime.timedelta(
                days=random.randint(0, 28),
                hours=random.randint(0, 24),
                minutes=random.randint(0, 60),
                seconds=random.randint(0, 60),
            )
            et = datetime.timedelta(
                days=random.randint(0, 28),
                hours=random.randint(0, 24),
                minutes=random.randint(0, 60),
                seconds=random.randint(0, 60),
            )
            dr = TaskDateRange(
                start=datetime.datetime.now() - st,
                end=datetime.datetime.now() + et
            )
            u.date_ranges.append(dr)
            date_ranges.append(dr)
        tasks.append(u)
    session.add_all(tasks)
    session.commit()

    # Task Dependency
    task_depend = []
    entries = defaultdict(list)
    for task in tasks:
        for i in range(2):
            depend_on = task
            while depend_on.id == task.id or depend_on.id in (
                        entries.get(task.id) or []):
                depend_on = random.choice(tasks)
            td = TaskDependency(task, depend_on)
            entries[task.id].append(depend_on.id)
            task_depend.append(td)
    session.add_all(task_depend)
    session.commit()
    return


def queryTasks(session):
    # Query all task categories
    q = session.query(TaskCategory)
    categories = q.all()
    print '=' * 80
    print 'TaskCategories...'
    for category in categories:
        print '-' * 25
        print 'name:', category.name
        print 'tasks:', category.tasks
        
    # Query all task statuses
    q = session.query(TaskStatus)
    statuses = q.all()
    print '=' * 80
    print 'TaskStatuses...'
    for status in statuses:
        print '-' * 25
        print 'name:', status.name
        print 'tasks:', status.tasks
    
    # Query all tasks
    q = session.query(Task)
    all_tasks = q.all()
    print '=' * 80
    print 'Tasks...'
    for task in all_tasks:
        print '-' * 25
        print 'name:', task.name
        print 'users:', task.users
        print 'department:', task.department
        print 'date_ranges:', task.date_ranges
        print 'task_status:', task.task_status
        print 'task_category:', task.task_category

    # Query all task dependencies
    q = session.query(TaskDependency)
    all_task_depends = q.all()
    print '=' * 80
    print 'Task Dependencies...'
    for td in all_task_depends:
        print '-' * 25
        src = td.source_task
        for dst in src.destination_neighbours():
            print '{0} --> {1}'.format(src.name, dst.name)
    return


def createProjects(session):
    cfg_status = session.query(ConfigFileStatus).filter(
        ConfigFileStatus.name == 'active').all()

    # Project Statuses
    names = ['complete', 'in_progress', 'not_started']
    labels = ['Project Complete', 'Project In-Progress', 'Project Not Started']
    descs = ['The project is finished',
             'The project is currently being worked on',
             'The project is not started yet']
    proj_statuses = createGenericStatus(
        ProjectStatus,
        names=names,
        labels=labels,
        descriptions=descs
    )
    session.add_all(proj_statuses)
    session.commit()

    # Project Category
    names = ['feature', 'commercial']
    proj_categories = []
    for name in names:
        pt = ProjectCategory(name=name)
        proj_categories.append(pt)
    session.add_all(proj_categories)
    session.commit()

    # Operating Systems
    names = ['centos6_linux', 'mac_osx_10_6', 'windows_10']
    op_systems = []
    for name in names:
        op_sys = OperatingSystem(name=name)
        op_systems.append(op_sys)
    session.add_all(op_systems)
    session.commit()

    # Projects
    names = ['dunkirk',
             'babydriver',
             'seashore']
    labels = ['Dunkirk',
              'Baby Driver',
              'Seashore']
    descs = ['This project is totally awesome!',
             'description',
             'more description']
    projs = []
    for name, label, desc in zip(names, labels, descs):
        cfg, cfgv = createConfigFile(session, name=name,  status=cfg_status[0])
        p = Project(
            name=name,
            label=label,
            description=desc,
            project_category=random.choice(proj_categories),
            project_status=random.choice(proj_statuses),
            config_file=cfg,
        )
        projs.append(p)
    session.add_all(projs)
    session.commit()

    # Storage Root
    roots = ['/data/projects', '/Volumes/projects', 'Z:/']
    storage_roots = []
    for root, op_sys in zip(roots, op_systems):
        for proj in projs:
            name = '{0}_{1}'.format(proj.name, op_sys.name)
            sr = StorageRoot(
                name=name,
                operating_system=op_sys,
                project=proj,
                root_path=root,
            )
            storage_roots.append(sr)
    session.add_all(storage_roots)
    session.commit()
    return


def queryProjects(session):
    # Query Projects...
    q = session.query(Project)
    all_projects = q.all()
    print '=' * 80
    print 'Projects...'
    for proj in all_projects:
        print '-' * 25
        print 'name:', proj.name
        print 'label:', proj.label
        print 'description:', proj.description
        print 'storage_roots:', proj.storage_roots
    return


def createAssets(session):
    projs = session.query(Project).all()
    cfg_status = session.query(ConfigFileStatus).filter(
        ConfigFileStatus.name == 'active').all()

    # Asset Statuses
    names = ['complete', 'in_progress', 'not_started']
    labels = ['Asset Complete', 'Asset In-Progress', 'Asset Not Started']
    statuses = createGenericStatus(
        AssetStatus,
        names=names,
        labels=labels
    )
    session.add_all(statuses)
    session.commit()

    # Asset Categories
    names = ['char', 'env', 'prop']
    labels = ['Character', 'Environment', 'Prop']
    categories = []
    for name, label in zip(names, labels):
        cfg, cfgv = createConfigFile(session, name=name, status=cfg_status[0])
        ac = AssetCategory(
            name=name,
            label=label
        )
        categories.append(ac)
    session.add_all(categories)
    session.commit()

    # Assets
    names = ['john', 'newyork', 'sally', 'gun', 'laptop']
    categories = [categories[0], categories[1], categories[0],
                  categories[2], categories[2]]
    assets = []
    for proj in projs:
        for name, category in zip(names, categories):
            a = Asset(
                name=name,
                project=proj,
                asset_category=category,
                asset_status=random.choice(statuses)
            )
            assets.append(a)
    session.add_all(assets)
    session.commit()
    return


def queryAssets(session):
    # Query...
    q = session.query(Asset)
    all_assets = q.all()
    print '=' * 80
    print 'Assets...'
    for asset in all_assets:
        print '-' * 25
        print 'name:', asset.name
        print 'description:', asset.description
    return


def createMediaVersions(session):
    # projs = session.query(Project).all()
    shots = session.query(Shot).all()
    assets = session.query(Asset).all()
    tasks = session.query(Task).all()

    # Image Resolution
    ir_hd1080 = ImageResolution(
        name='HD 1080p',
        width=1920,
        height=1080,
        pixel_aspect=1.0
    )
    ir_hd720 = ImageResolution(
        name='HD 720p',
        width=1280,
        height=720,
        pixel_aspect=1.0
    )
    ir_cine = ImageResolution(
        name='Cinema',
        width=2048,
        height=856,
        pixel_aspect=1.0
    )
    image_reses = [ir_hd1080, ir_hd720, ir_cine]
    session.add_all(image_reses)
    session.commit()

    # Media Statuses
    media_version_names = ['reviewed', 'pending', 'not_for_review', 'approved']
    labels = ['Reviewed', 'Pending', 'Not For Review', 'Approved']
    statuses = createGenericStatus(
        MediaVersionStatus,
        names=media_version_names,
        labels=labels
    )
    session.add_all(statuses)
    session.commit()

    # Media Version Categories
    media_version_names = ['viewport_preview', 'render',
             'previs', 'composite', 'client_plate']
    labels = ['Viewport Preview', '3D Render',
              'Pre-Visualisation', '2D composite', 'client_plate']
    categories = []
    for media_version_name, label in zip(media_version_names, labels):
        ac = MediaVersionCategory(
            name=media_version_name,
            label=label
        )
        categories.append(ac)
    session.add_all(categories)
    session.commit()

    # Media Names
    names = ['layout', 'comp', 'animation', 'model', 'shader']
    media_version_names = []
    for name in names:
        m = MediaVersionName(
            name=name
        )
        media_version_names.append(m)
    session.add_all(media_version_names)
    session.commit()

    # Media Subnames
    names = ['media_subname']
    media_version_subnames = []
    for name in names:
        m = MediaVersionName(
            name=name
        )
        media_version_subnames.append(m)
    session.add_all(media_version_names)
    session.commit()

    # Media Versions
    min_value = 1
    max_value = 3
    media_versions = []
    for media_version_name in media_version_names:
        # app_ver = random.randint(min_value, max_value)
        # app_rev = random.randint(min_value, max_value)
        for i in range(min_value, random.randint(min_value, max_value)):
            for j in range(min_value, random.randint(min_value, max_value)):
                mv = MediaVersion(
                    media_version_name=media_version_name,
                    version=i,
                    revision=j,
                    task=random.choice(tasks),
                    media_version_status=random.choice(statuses),
                    media_version_category=random.choice(categories),
                    image_resolution=random.choice(image_reses)
                )
                media_versions.append(mv)
    session.add_all(media_versions)
    session.commit()
    return


def queryMediaVersions(session):
    # Image Resolution
    q = session.query(ImageResolution)
    all_reses = q.all()
    print '=' * 80
    print 'ImageResolution...'
    for res in all_reses:
        print '-' * 25
        print 'name:', res.name
        print 'width:', res.width
        print 'height:', res.height
        print 'pixel_aspect:', res.pixel_aspect

    # Media Version Status
    q = session.query(MediaVersionStatus)
    statuses = q.all()
    print '=' * 80
    print 'MediaVersionStatus...'
    for status in statuses:
        print '-' * 25
        print 'name:', status.name
        print 'label:', status.label
        print 'description:', status.description
        
    # Media Version Category
    q = session.query(MediaVersionCategory)
    categories = q.all()
    print '=' * 80
    print 'MediaVersionCategory...'
    for category in categories:
        print '-' * 25
        print 'name:', category.name
        print 'label:', category.label
        print 'description:', category.description

    # Media Names
    q = session.query(MediaVersionName)
    names = q.all()
    print '=' * 80
    print 'MediaVersionName...'
    for name in names:
        print '-' * 25
        print 'name:', name.name
        
    # Media Subnames
    q = session.query(MediaVersionSubname)
    subnames = q.all()
    print '=' * 80
    print 'MediaVersionSubname...'
    for subname in subnames:
        print '-' * 25
        print 'name:', subname.subname

    # Media Versions
    q = session.query(MediaVersion)
    all_media_versions = q.all()
    print '=' * 80
    print 'MediaVersion...'
    for ver in all_media_versions:
        print 'name:', ver.media_version_name
        print 'subname:', ver.media_version_subname
        print 'version:', ver.version
        print 'revision:', ver.revision
        print 'status:', ver.media_version_status
        print 'category:', ver.media_version_category
        print 'task:', ver.task
        print 'res:', ver.image_resolution
    return


def createSequences(session):
    projs = session.query(Project).all()
    cfg_status = session.query(ConfigFileStatus) \
        .filter(ConfigFileStatus.name == 'active').all()

    # Sequence Statuses
    names = ['complete', 'in_progress', 'not_started']
    labels = ['Sequence Complete',
              'Sequence In-Progress',
              'Sequence Not Started']
    descs = ['The sequence is finished',
             'The sequence is currently being worked on',
             'The sequence is not started yet']
    sequence_statuses = createGenericStatus(
        SequenceStatus,
        names=names,
        labels=labels,
        descriptions=descs
    )
    session.add_all(sequence_statuses)
    session.commit()

    # Sequence Category
    names = ['normal']
    sequence_categories = []
    for name in names:
        pt = SequenceCategory(name=name)
        sequence_categories.append(pt)
    session.add_all(sequence_categories)
    session.commit()

    # Sequences
    names = [
        'sh', 'fin', 'sq', 'pd', 'zb'
    ]
    seqs = []
    for proj in projs:
        for name in names:
            cfg, cfgv = createConfigFile(session, name=name, status=cfg_status[0])
            status = random.choice(sequence_statuses)
            category = random.choice(sequence_categories)
            seq = Sequence(
                name=name,
                sequence_status=status,
                sequence_category=category,
                config_file=cfg,
                project=proj,
            )
            seqs.append(seq)
    session.add_all(seqs)
    session.commit()
    return


def querySequences(session):
    # Query Sequence Status...
    q = session.query(SequenceStatus)
    statuses = q.all()
    print '=' * 80
    print 'SequenceStatus...'
    for status in statuses:
        print '-' * 25
        print 'name:', status.name

    # Query Sequence Categories...
    q = session.query(SequenceCategory)
    categories = q.all()
    print '=' * 80
    print 'SequenceCategory...'
    for category in categories:
        print '-' * 25
        print 'name:', category.name

    # Query Sequence...
    q = session.query(Sequence)
    all_sequences = q.all()
    print '=' * 80
    print 'Sequence...'
    for sequence in all_sequences:
        print '-' * 25
        print 'name:', sequence.name
        print 'status:', sequence.sequence_status
        print 'category:', sequence.sequence_category
    return


def createScenes(session):
    projs = session.query(Project).all()
    cfg_status = session.query(ConfigFileStatus) \
        .filter(ConfigFileStatus.name == 'active').all()

    # Scene Statuses
    names = ['complete', 'in_progress', 'not_started']
    labels = ['Scene Complete',
              'Scene In-Progress',
              'Scene Not Started']
    descs = ['The scene is finished',
             'The scene is currently being worked on',
             'The scene is not started yet']
    scene_statuses = createGenericStatus(
        SceneStatus,
        names=names,
        labels=labels,
        descriptions=descs
    )
    session.add_all(scene_statuses)
    session.commit()

    # Scene Category
    names = ['normal']
    scene_categories = []
    for name in names:
        pt = SceneCategory(name=name)
        scene_categories.append(pt)
    session.add_all(scene_categories)
    session.commit()

    # Scenes
    names = [
        'mainHall', 'corridor', 'spookyDoor',
    ]
    scns = []
    for proj in projs:
        for name in names:
            cfg, cfgv = createConfigFile(session, name=name, status=cfg_status[0])
            status = random.choice(scene_statuses)
            category = random.choice(scene_categories)
            scn = Scene(
                name=name,
                scene_status=status,
                scene_category=category,
                config_file=cfg,
                project=proj,
            )
            scns.append(scn)
    session.add_all(scns)
    session.commit()
    return


def queryScenes(session):
    # Query Scene Status...
    q = session.query(SceneStatus)
    statuses = q.all()
    print '=' * 80
    print 'SceneStatus...'
    for status in statuses:
        print '-' * 25
        print 'name:', status.name

    # Query Scene Categories...
    q = session.query(SceneCategory)
    categories = q.all()
    print '=' * 80
    print 'SceneCategory...'
    for category in categories:
        print '-' * 25
        print 'name:', category.name

    # Query Scene...
    q = session.query(Scene)
    all_scenes = q.all()
    print '=' * 80
    print 'Scene...'
    for scene in all_scenes:
        print '-' * 25
        print 'name:', scene.name
        print 'status:', scene.scene_status
        print 'category:', scene.scene_category
    return


def createShots(session):
    projs = session.query(Project).all()
    tasks = session.query(Task).all()
    cfg_status = session.query(ConfigFileStatus)\
        .filter(ConfigFileStatus.name == 'active').all()

    # Shot Statuses
    names = ['complete', 'in_progress', 'not_started']
    labels = ['Shot Complete', 'Shot In-Progress', 'Shot Not Started']
    descs = ['The shot is finished',
             'The shot is currently being worked on',
             'The shot is not started yet']
    shot_statuses = createGenericStatus(
        ShotStatus,
        names=names,
        labels=labels,
        descriptions=descs
    )
    session.add_all(shot_statuses)
    session.commit()

    # Shot Category
    names = ['normal', 'test']
    shot_categories = []
    for name in names:
        pt = ShotCategory(name=name)
        shot_categories.append(pt)
    session.add_all(shot_categories)
    session.commit()

    # Shots
    names = [
        'sh010', 'sh020', 'sh030', 'sh040',
        'sh050', 'sh060', 'sh070', 'sh080',
        'sh090', 'sh100', 'sh110', 'sh120',
        'sh130', 'sh140', 'sh150', 'sh160',
        'sh170', 'sh180', 'sh190', 'sh200',
    ]
    shots = []
    for proj in projs:
        seqs = session.query(Sequence).filter(Sequence.project_id == proj.id).all()
        scns = session.query(Scene).filter(Scene.project_id == proj.id).all()
        for name in names:
            cfg, cfgv = createConfigFile(session, name=name, status=cfg_status[0])
            seq = random.choice(seqs)
            scn = random.choice(scns)
            assert seq.project_id == scn.project_id

            sht = Shot(
                name=name,
                shot_status=random.choice(shot_statuses),
                shot_category=random.choice(shot_categories),
                config_file=cfg,
                sequence=seq,
                scene=scn,
            )

            for i in range(random.randint(1, 2)):
                task = random.choice(tasks)
                sht.tasks.append(task)
            shots.append(sht)
    session.add_all(shots)
    session.commit()
    return


def queryShots(session):
    # Query Shot Status...
    q = session.query(ShotStatus)
    statuses = q.all()
    print '=' * 80
    print 'ShotStatus...'
    for status in statuses:
        print '-' * 25
        print 'name:', status.name

    # Query Shot Categories...
    q = session.query(ShotCategory)
    categories = q.all()
    print '=' * 80
    print 'ShotCategory...'
    for category in categories:
        print '-' * 25
        print 'name:', category.name

    # Query Shot...
    q = session.query(Shot)
    all_shots = q.all()
    print '=' * 80
    print 'Shot...'
    for shot in all_shots:
        print '-' * 25
        print 'name:', shot.name
        print 'status:', shot.shot_status
        print 'category:', shot.shot_category
        print 'tasks:', shot.tasks
        print 'project:', shot.project
        print 'sequence:', shot.sequence
        print 'scene:', shot.scene
        assert shot.sequence.project_id == shot.scene.project_id
        assert shot.project.id == shot.scene.project_id
        assert shot.project.id == shot.sequence.project_id
    return


def createAssetDatas(session):
    projs = session.query(Project).all()

    # Asset Data Statuses
    names = ['active', 'deactive']
    labels = ['Active', 'Deactive']
    statuses = createGenericStatus(
        AssetDataStatus,
        names=names,
        labels=labels
    )
    session.add_all(statuses)
    session.commit()

    # Asset Data Names...
    names = []
    subnames = []
    variants = []
    reses = []
    insts = []
    types = []
    for n in ['john', 'newyork', 'sally', 'gun', 'laptop']:
        names.append(AssetDataName(name=n))
    for n in ['main']:
        subnames.append(AssetDataSubname(name=n))
    for n in ['main', 'red', 'green']:
        variants.append(AssetDataVariant(name=n))
    for n in ['lowres', 'highres']:
        reses.append(AssetDataResolution(name=n))
    for n in ['001', '002', '003', '004', '005', 'bg', 'fg']:
        insts.append(AssetDataInstance(name=n))
    for n in ['anim', 'cache', 'rig', 'model']:
        types.append(AssetDataType(name=n))

    # Asset Data
    min_value = 1
    max_value = 10
    record = names + subnames + variants + reses + insts + types
    comment = 'Comment'
    for proj in projs:

        # Project
        shots = session.query(Shot) \
            .join(Shot.sequence, Sequence.project) \
            .filter(Project.id == proj.id).all()
        for name in names:
            assets = session.query(Asset).filter(Asset.project_id == proj.id,
                                                 Asset.name == name.name).all()
            asset = assets[0]

            shot = random.choice(shots)
            ad = AssetData(
                asset=asset,
                shot=shot,
                asset_data_name=random.choice(names),
                asset_data_subname=random.choice(subnames),
                asset_data_variant=random.choice(variants),
                asset_data_instance=random.choice(insts),
                asset_data_type=random.choice(types),
                asset_data_resolution=random.choice(reses),
                asset_data_status=random.choice(statuses)
            )

            app_ver = random.randint(min_value, max_value)
            app_rev = random.randint(min_value, max_value)

            frz_ver = random.randint(min_value, max_value)
            frz_rev = random.randint(min_value, max_value)

            for i in range(min_value, random.randint(min_value, max_value)):
                for j in range(min_value, random.randint(min_value, max_value)):
                    approved = i == app_ver and j == app_rev
                    frozen = i == frz_ver and j == frz_rev
                    v = AssetDataVersion(
                        asset_data=ad,
                        version=i,
                        revision=j,
                        approved=approved,
                        frozen=frozen,
                        comment=comment
                    )
                    record.append(v)
            record.append(ad)
    session.add_all(record)
    session.commit()
    return


def queryAssetDatas(session):
    q = session.query(Asset)
    assets = q.all()
    print '=' * 80
    print 'Assets...'
    for asset in assets:
        print '-' * 25
        print 'project:', asset.project.name
        print 'name:', asset.name
        print 'description:', asset.description
        print 'category:', asset.asset_category.name
        print 'status:', asset.asset_status.name

    q = session.query(AssetDataName)
    names = q.all()
    print '=' * 80
    print 'AssetDataNames...'
    for name in names:
        print '-' * 25
        print 'name:', name.name

    q = session.query(AssetDataSubname)
    names = q.all()
    print '=' * 80
    print 'AssetDataSubnames...'
    for name in names:
        print '-' * 25
        print 'name:', name.name

    q = session.query(AssetDataVariant)
    variants = q.all()
    print '=' * 80
    print 'AssetDataVariant...'
    for variant in variants:
        print '-' * 25
        print 'name:', variant.name

    q = session.query(AssetDataResolution)
    resolutions = q.all()
    print '=' * 80
    print 'AssetDataResolutions...'
    for resolution in resolutions:
        print '-' * 25
        print 'name:', resolution.name

    q = session.query(AssetDataInstance)
    instances = q.all()
    print '=' * 80
    print 'AssetDataInstances...'
    for instance in instances:
        print '-' * 25
        print 'name:', instance.name

    q = session.query(AssetDataType)
    types = q.all()
    print '=' * 80
    print 'AssetDataTypes...'
    for type in types:
        print '-' * 25
        print 'name:', type.name

    q = session.query(AssetData)
    assetdatas = q.all()
    print '=' * 80
    print 'AssetDatas...'
    for assetdata in assetdatas:
        print '-' * 25
        print 'name:', assetdata.asset_data_name
        print 'subname:', assetdata.asset_data_subname
        print 'variant:', assetdata.asset_data_variant
        print 'instance:', assetdata.asset_data_instance
        print 'resolution:', assetdata.asset_data_resolution
        print 'type:', assetdata.asset_data_type

    q = session.query(AssetDataVersion)
    versions = q.all()
    print '=' * 80
    print 'AssetDataVersions...'
    for ver in versions:
        print '-' * 25
        print 'asset_data:', ver.asset_data
        print 'task:', ver.task
        print 'media_version:', ver.media_version
        print 'version:', ver.version
        print 'revision:', ver.revision
        print 'approved:', ver.approved
        print 'frozen:', ver.frozen

    print '=' * 80
    print 'Asset Tree...'
    indent = 0
    space = '  '
    projs = session.query(Project).all()
    for proj in projs:
        print (space * indent) + 'Project:', proj
        indent = 1

        shots = session.query(Shot) \
            .join(Shot.sequence, Sequence.project) \
            .filter(Sequence.project_id == proj.id).all()
        for shot in shots:
            indent = 2
            print (space * indent) + 'Shot:', shot
            q = session.query(AssetData).filter(AssetData.shot_id == shot.id)
            assetdatas = q.all()
            for assetdata in assetdatas:
                indent = 3
                x = (space * indent)
                print x + 'AssetData:', assetdata
                print x + ' > name:', assetdata.asset_data_name.name
                print x + ' > subname:', assetdata.asset_data_subname.name
                print x + ' > variant:', assetdata.asset_data_variant.name
                print x + ' > instance:', assetdata.asset_data_instance.name
                print x + ' > resolution:', assetdata.asset_data_resolution.name
                print x + ' > type:', assetdata.asset_data_type.name

                q = session.query(AssetDataVersion) \
                    .join(AssetDataVersion.asset_data) \
                    .filter(AssetData.id == assetdata.id)
                assetdatavers = q.all()
                for assetdataver in assetdatavers:
                    indent = 4
                    if assetdataver.approved:
                        print (space * indent) + 'AssetDataVersion:', assetdataver

        assets = session.query(Asset) \
            .join(Asset.project) \
            .filter(Asset.project_id == proj.id).all()
        for asset in assets:
            indent = 2
            print (space * indent) + 'Asset:', asset

            q = session.query(AssetData).filter(AssetData.asset_id == asset.id)
            assetdatas = q.all()
            for assetdata in assetdatas:
                indent = 3
                x = (space * indent)
                print x + 'AssetData:', assetdata
                print x + ' > name:', assetdata.asset_data_name.name
                print x + ' > subname:', assetdata.asset_data_subname.name
                print x + ' > variant:', assetdata.asset_data_variant.name
                print x + ' > instance:', assetdata.asset_data_instance.name
                print x + ' > resolution:', assetdata.asset_data_resolution.name
                print x + ' > type:', assetdata.asset_data_type.name

                q = session.query(AssetDataVersion) \
                    .join(AssetDataVersion.asset_data) \
                    .filter(AssetData.id == assetdata.id)
                assetdatavers = q.all()
                # print 'assetdatavers:', assetdatavers
                for assetdataver in assetdatavers:
                    indent = 4
                    if assetdataver.approved:
                        print (space * indent) + 'AssetDataVersion:', assetdataver
    return


def main():
    # print 'args', sys.argv
    reset_tables = False
    if len(sys.argv) > 1:
        reset_tables = bool(str(sys.argv[1]))

    url = setup.get_database_url()
    engine = create_engine(url, echo=setup.ECHO)

    # Reset tables
    if reset_tables is True:
        base.dropTables(engine)
        base.createTables(engine)

    session = setup.get_session()

    createUsers(session)
    createTasks(session)
    createConfigFiles(session)
    createProjects(session)
    createAssets(session)
    createSequences(session)
    createScenes(session)
    createShots(session)
    createMediaVersions(session)
    createAssetDatas(session)

    queryUsers(session)
    queryTasks(session)
    queryConfigFiles(session)
    queryProjects(session)
    queryAssets(session)
    querySequences(session)
    queryScenes(session)
    queryShots(session)
    queryMediaVersions(session)
    queryAssetDatas(session)


if __name__ == '__main__':
    main()
