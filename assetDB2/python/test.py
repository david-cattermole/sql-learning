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

import assetDB.setup as setup
import assetDB.models.modelbase as base
from assetDB.models import *
import assetDB.config as config


def createTasks(session):
    names = ['model', 'camera', 'animation',
             'rig', 'shader', 'texture',
             'lighting', 'render', 'effects',
             'comp']
    tasks = []
    for name in names:
        t = Task(name=name)
        tasks.append(t)
    session.add_all(tasks)
    session.commit()
    return


def queryTasks(session):
    q = session.query(Task)
    all_tasks = q.all()
    print '=' * 80
    print 'Tasks...'
    for task in all_tasks:
        print '-' * 25
        print 'name:', task.name
    return


def createMediaVersions(session):
    names = ['layout', 'comp', 'animation', 'model', 'shader']
    media_versions = []
    for name in names:
        mv = MediaVersion(name=name)
        media_versions.append(mv)
    session.add_all(media_versions)
    session.commit()
    return


def queryMediaVersions(session):
    q = session.query(MediaVersion)
    all_media_versions = q.all()
    print '=' * 80
    print 'MediaVersion...'
    for ver in all_media_versions:
        print 'name:', ver.name
    return


def createProjects(session):
    names = ['dunkirk', 'babydriver', 'seashore']
    projs = []
    for name in names:
        p = Project(name=name)
        projs.append(p)
    session.add_all(projs)
    session.commit()
    return


def queryProjects(session):
    q = session.query(Project)
    all_projects = q.all()
    print '=' * 80
    print 'Projects...'
    for proj in all_projects:
        print '-' * 25
        print 'name:', proj.name
    return


def createSequences(session):
    names = ['sh', 'fin', 'sq', 'pd', 'zb']
    seqs = []
    for name in names:
        seq = Sequence(name=name)
        seqs.append(seq)
    session.add_all(seqs)
    session.commit()
    return


def querySequences(session):
    q = session.query(Sequence)
    all_sequences = q.all()
    print '=' * 80
    print 'Sequence...'
    for seq in all_sequences:
        print '-' * 25
        print 'name:', seq.name
    return


def createShots(session):
    names = [
        'sh010', 'sh020', 'sh030', 'sh040',
        'sh050', 'sh060', 'sh070', 'sh080',
        'sh090', 'sh100', 'sh110', 'sh120',
        'sh130', 'sh140', 'sh150', 'sh160',
        'sh170', 'sh180', 'sh190', 'sh200',
    ]
    shots = []
    for name in names:
        sht = Shot(name=name)
        shots.append(sht)
    session.add_all(shots)
    session.commit()
    return


def queryShots(session):
    q = session.query(Shot)
    all_shots = q.all()
    print '=' * 80
    print 'Shot...'
    for shot in all_shots:
        print '-' * 25
        print 'name:', shot.name
    return


def createNames(session):
    names = []
    subnames = []
    variants = []
    reses = []
    insts = []
    types = []
    for n in ['john', 'newyork', 'sally', 'gun', 'laptop']:
        names.append(Name(name=n))
    for n in ['main']:
        subnames.append(Subname(name=n))
    for n in ['main', 'red', 'green']:
        variants.append(Variant(name=n))
    for n in ['lowres', 'highres']:
        reses.append(Resolution(name=n))
    for n in ['001', '002', '003', '004', '005', 'bg', 'fg']:
        insts.append(Instance(name=n))
    for n in ['anim', 'cache', 'rig', 'model']:
        types.append(Type(name=n))

    record = names + subnames + variants + reses + insts + types
    session.add_all(record)
    session.commit()
    return


def queryNames(session):
    q = session.query(Name)
    names = q.all()
    print '=' * 80
    print 'Names...'
    for name in names:
        print '-' * 25
        print 'name:', name.name

    q = session.query(Subname)
    names = q.all()
    print '=' * 80
    print 'Subnames...'
    for name in names:
        print '-' * 25
        print 'name:', name.name

    q = session.query(Variant)
    variants = q.all()
    print '=' * 80
    print 'Variant...'
    for variant in variants:
        print '-' * 25
        print 'name:', variant.name

    q = session.query(Resolution)
    resolutions = q.all()
    print '=' * 80
    print 'Resolutions...'
    for resolution in resolutions:
        print '-' * 25
        print 'name:', resolution.name

    q = session.query(Instance)
    instances = q.all()
    print '=' * 80
    print 'Instances...'
    for instance in instances:
        print '-' * 25
        print 'name:', instance.name

    q = session.query(Type)
    types = q.all()
    print '=' * 80
    print 'Types...'
    for type in types:
        print '-' * 25
        print 'name:', type.name
    return


def createAssets(session):
    # Tags
    approved_tag = Tag(name='approved')
    frozen_tag = Tag(name='frozen')
    latest_tag = Tag(name='latest')
    high_priority_tag = Tag(name='high_priority')
    low_priority_tag = Tag(name='low_priority')
    session.add_all([approved_tag, frozen_tag, latest_tag,
                     high_priority_tag, low_priority_tag])

    # Key
    start_frame_key = Key(name='start_frame')
    end_frame_key = Key(name='end_frame')
    samples_key = Key(name='samples')
    priority_key = Key(name='priority')
    session.add_all([start_frame_key, end_frame_key, samples_key, priority_key])
    session.commit()

    min_value = 1
    max_value = 10
    record = []
    comment = 'Comment'

    projects = session.query(Project).all()
    sequences = session.query(Sequence).all()
    shots = session.query(Shot).all()

    names = session.query(Name).all()
    subnames = session.query(Subname).all()
    variants = session.query(Variant).all()
    reses = session.query(Resolution).all()
    insts = session.query(Instance).all()
    types = session.query(Type).all()

    media_versions = session.query(MediaVersion).all()
    tasks = session.query(Task).all()

    assets = []
    asset_versions = []
    for name in names:
        a = Asset(
            project=random.choice(projects),
            sequence=random.choice(sequences),
            shot=random.choice(shots),
            name=name,
            subname=random.choice(subnames),
            variant=random.choice(variants),
            instance=random.choice(insts),
            type=random.choice(types),
            resolution=random.choice(reses),
        )
        assets.append(a)
        record.append(a)

        priority = random.randint(1, 100)
        akv = AssetKeyValue(priority_key, Value(priority), a)
        record.append(akv)

        priority_tag = high_priority_tag
        if priority < 50:
            priority_tag = low_priority_tag
        at = AssetTag(priority_tag, a)
        record.append(at)

        app_ver = random.randint(min_value, max_value)

        last_value = random.randint(min_value, max_value)
        for i in range(min_value, last_value + 1):
            approved = i == app_ver
            latest = i == last_value
            av = AssetVersion(
                asset=a,
                version=i,
                comment=comment,
                media_version=random.choice(media_versions),
                task=random.choice(tasks),
            )
            asset_versions.append(av)
            record.append(av)

            start_frame = random.randint(1001, 1101)
            end_frame = random.randint(start_frame, 1101)
            avkv = AssetVersionKeyValue(start_frame_key, Value(start_frame), av)
            record.append(avkv)

            avkv = AssetVersionKeyValue(end_frame_key, Value(end_frame), av)
            record.append(avkv)

            samples = random.randint(1, 1024)
            avkv = AssetVersionKeyValue(samples_key, Value(samples), av)
            record.append(avkv)

            priority = abs(random.random()) * float(random.randint(1, 100))
            avkv = AssetVersionKeyValue(priority_key, Value(priority), av)
            record.append(avkv)

            if approved:
                avst = AssetVersionStatusTag(approved_tag, av)
                record.append(avst)

            if latest:
                avst = AssetVersionStatusTag(latest_tag, av)
                record.append(avst)

    # Asset Dependencies
    for asset in assets:
        src_asset = random.choice(assets)
        if src_asset != asset:
            ad = AssetDependency(src_asset, asset)
            record.append(ad)

    # Asset Version Dependencies
    for asset_version in asset_versions:
        src_asset_version = random.choice(asset_versions)
        if src_asset_version != asset_version:
            avd = AssetVersionDependency(src_asset_version, asset_version)
            record.append(avd)

    session.add_all(record)
    session.commit()
    return


def queryAssets(session):
    q = session.query(Asset)
    assets = q.all()
    print '=' * 80
    print 'Assets...'
    for asset in assets:
        print '-' * 25
        print 'project:', asset.project.name
        print 'sequence:', asset.sequence.name
        print 'shot:', asset.shot.name
        print 'name:', asset.name
        print 'subname:', asset.subname
        print 'instance:', asset.instance
        print 'variant:', asset.variant
        print 'resolution:', asset.resolution
        print 'type:', asset.type

    q = session.query(AssetVersion)
    asset_versions = q.all()
    print '=' * 80
    print 'AssetVersions...'
    for ver in asset_versions:
        print '-' * 25
        print 'asset:', ver.asset
        print 'task:', ver.task
        print 'media_version:', ver.media_version
        print 'version:', ver.version
        incoming = []
        for i in ver.incoming_assets:
            name = '%s -> %s' % (i.source.path, i.destination.path)
            incoming.append(name)
        outgoing = []
        for i in ver.outgoing_assets:
            name = '%s -> %s' % (i.source.path, i.destination.path)
            outgoing.append(name)
        print 'incoming assets:', incoming
        print 'outgoing assets:', outgoing

    print '=' * 80
    print 'Asset Tree...'
    space = '  '
    indent = 0
    q = session.query(Asset)
    assets = q.all()
    for asset in assets:
        indent = 0
        x = (space * indent)
        print x + 'Asset:', asset
        print x + ' > project:', asset.project.name
        print x + ' > sequence:', asset.sequence.name
        print x + ' > shot:', asset.shot.name
        print x + ' > name:', asset.name.name
        print x + ' > subname:', asset.subname.name
        print x + ' > variant:', asset.variant.name
        print x + ' > instance:', asset.instance.name
        print x + ' > resolution:', asset.resolution.name
        print x + ' > type:', asset.type.name

        q = session.query(AssetVersion) \
            .join(AssetVersion.asset) \
            .filter(Asset.id == asset.id)
        asset_versions = q.all()
        for version in asset_versions:
            indent = 1
            print (space * indent) + 'AssetVersion:', version

    print '=' * 80
    print 'Asset Paths...'
    q = session.query(Asset)
    assets = q.all()
    for asset in assets:
        # project = asset.project.name
        # sequence = asset.sequence.name
        # shot = asset.shot.name
        # name = asset.name.name
        # subname = asset.subname.name
        # variant = asset.variant.name
        # instance = asset.instance.name
        # resolution = asset.resolution.name
        # type = asset.type.name

        tags = asset.tags
        tag_names = []
        for tag in tags:
            tag_names.append(tag.name)

        key_values = asset.key_values
        key_value_names = []
        for key_value in key_values:
            kv_name = '%s:%s' % (key_value.key.name, key_value.value.value)
            key_value_names.append(kv_name)

        # path = os.path.join(os.path.sep, project, sequence, shot,
        #                     name, subname, instance, variant, resolution,
        #                     type)
        path = asset.path
        print path, str(tag_names), str(key_value_names)

    print '=' * 80
    print 'Asset Version Paths...'
    q = session.query(Asset)
    assets = q.all()
    for asset in assets:
        q = session.query(AssetVersion) \
            .join(AssetVersion.asset) \
            .filter(Asset.id == asset.id)
        asset_versions = q.all()
        for asset_version in asset_versions:
            version_tags = asset_version.status_tags
            version_tag_names = []
            for tag in version_tags:
                version_tag_names.append(tag.name)

            version_key_values = asset_version.key_values
            version_key_value_names = []
            for key_value in version_key_values:
                kv_name = '%s:%s' % (key_value.key.name, key_value.value.value)
                version_key_value_names.append(kv_name)

            path = asset_version.path
            print path, str(version_tag_names), str(version_key_value_names)

    return


def main():
    url = setup.get_database_url()
    engine = create_engine(url, echo=setup.ECHO)
    session = setup.get_session()

    base.dropTables(engine)
    base.createTables(engine)

    createTasks(session)
    createMediaVersions(session)
    createProjects(session)
    createSequences(session)
    createShots(session)
    createNames(session)
    createAssets(session)

    queryTasks(session)
    queryMediaVersions(session)
    queryProjects(session)
    querySequences(session)
    queryShots(session)
    queryNames(session)
    queryAssets(session)


if __name__ == '__main__':
    main()
