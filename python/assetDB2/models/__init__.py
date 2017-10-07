"""
All of the tables used in the database
"""

from assetDB2.models.asset import (
    Asset,
    AssetTag,
    AssetKeyValue,
    AssetDependency
)

from assetDB2.models.assetversion import (
    AssetVersion,
    AssetVersionTag,
    AssetVersionStatusTag,
    AssetVersionKeyValue,
    AssetVersionDependency
)

from assetDB2.models.names import (
    MediaVersion,
    Task,
    Project,
    Sequence,
    Shot,
    Name,
    Subname,
    Instance,
    Resolution,
    Type,
    Variant
)

from assetDB2.models.tags import (
    Tag,
    Value,
    Key,
)

__all__ = [
    'Asset',
    'AssetTag',
    'AssetKeyValue',
    'AssetDependency',

    'AssetVersion',
    'AssetVersionTag',
    'AssetVersionStatusTag',
    'AssetVersionKeyValue',
    'AssetVersionDependency',

    'MediaVersion',
    'Task',

    'Project',
    'Shot',
    'Sequence',

    'Name',
    'Subname',
    'Instance',
    'Resolution',
    'Type',
    'Variant',

    'Key',
    'Value',
    'Tag',

]


