"""
All of the tables used in the database
"""

from assetDB.tables.assetdata import (
    AssetData, AssetDataStatus,
    AssetDataName, AssetDataSubname, AssetDataInstance,
    AssetDataResolution, AssetDataType, AssetDataVariant, AssetDataVersion,
    AssetDataDependency
)
from assetDB.tables.shot import (
    Shot, ShotStatus, ShotCategory
)
from assetDB.tables.scene import (
    Scene, SceneStatus, SceneCategory
)
from assetDB.tables.sequence import (
    Sequence, SequenceStatus, SequenceCategory
)
from assetDB.tables.asset import (
    Asset, AssetStatus, AssetCategory
)
from assetDB.tables.media import (
    Media, MediaVersion, MediaVersionStatus, ImageResolution
)
from assetDB.tables.project import (
    Project, ProjectStatus, ProjectCategory, StorageRoot, OperatingSystem
)
from assetDB.tables.configfile import (
    ConfigFile, ConfigFileStatus, ConfigFileCategory, ConfigFileVersion
)
from assetDB.tables.task import (
    Task, TaskStatus, TaskDependency, TaskToUser, TaskDateRange
)
from assetDB.tables.user import (
    User, UserStatus, UserGroup, UserGroupToUser, Department, Site
)

__all__ = [
    'AssetData',
    'AssetDataStatus',
    'AssetDataName',
    'AssetDataSubname',
    'AssetDataInstance',
    'AssetDataResolution',
    'AssetDataType',
    'AssetDataVariant',
    'AssetDataVersion',
    'AssetDataDependency',

    'Shot',
    'ShotStatus',
    'ShotCategory',

    'Sequence',
    'SequenceStatus',
    'SequenceCategory',

    'Scene',
    'SceneStatus',
    'SceneCategory',

    'Asset',
    'AssetCategory',
    'AssetStatus',

    'Media',
    'MediaVersion',
    'MediaVersionStatus',
    'ImageResolution',

    'Project',
    'ProjectStatus',
    'ProjectCategory',
    'OperatingSystem',
    'StorageRoot',

    'ConfigFile',
    'ConfigFileVersion',
    'ConfigFileStatus',
    'ConfigFileCategory',

    'Task',
    'TaskStatus',
    'TaskDependency',
    'TaskToUser',
    'TaskDateRange',

    'User',
    'UserStatus',
    'UserGroup',
    'UserGroupToUser',
    'Site',
    'Department',
]


