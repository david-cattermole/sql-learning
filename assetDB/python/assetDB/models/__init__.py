"""
All of the tables used in the database
"""

from assetDB.models.assetdata import (
    AssetData,
    AssetDataStatus,
    AssetDataName,
    AssetDataSubname,
    AssetDataInstance,
    AssetDataResolution,
    AssetDataType,
    AssetDataVariant,
    AssetDataVersion,
    AssetDataDependency
)
from assetDB.models.shot import (
    Shot,
    ShotStatus,
    ShotCategory
)
from assetDB.models.scene import (
    Scene,
    SceneStatus,
    SceneCategory
)
from assetDB.models.sequence import (
    Sequence,
    SequenceStatus,
    SequenceCategory
)
from assetDB.models.asset import (
    Asset,
    AssetStatus,
    AssetCategory
)
from assetDB.models.mediaversion import (
    ImageResolution,
    MediaVersionName,
    MediaVersionSubname,
    MediaVersionCategory,
    MediaVersionStatus,
    MediaVersion,
)
from assetDB.models.project import (
    Project,
    ProjectStatus,
    ProjectCategory,
    StorageRoot,
    OperatingSystem
)
from assetDB.models.configfile import (
    ConfigFile,
    ConfigFileStatus,
    ConfigFileCategory,
    ConfigFileVersion
)
from assetDB.models.task import (
    Task,
    TaskStatus,
    TaskCategory,
    TaskDependency,
    TaskToUser,
    TaskDateRange
)
from assetDB.models.user import (
    User,
    UserStatus,
    UserGroup,
    UserGroupToUser,
    Department,
    Site
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

    'ImageResolution',
    'MediaVersionName',
    'MediaVersionSubname',
    'MediaVersionCategory',
    'MediaVersionStatus',
    'MediaVersion',

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
    'TaskCategory',
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


