from loguru import logger

EVENT_OFFSET = 100000


class APIErrorException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self):
        return self.error_message


# General errors

class InternalServerError(APIErrorException):
    ERROR_CODE = 0


class APIAccessDeactivated(APIErrorException):
    ERROR_CODE = 1


class JSONInvalid(APIErrorException):
    ERROR_CODE = 2


class APINameInvalid(APIErrorException):
    ERROR_CODE = 3


class APIVersionInvalid(APIErrorException):
    ERROR_CODE = 4


class RequestIDInvalid(APIErrorException):
    ERROR_CODE = 5


class RequestTypeMissingOrEmpty(APIErrorException):
    ERROR_CODE = 6


class RequestTypeUnknown(APIErrorException):
    ERROR_CODE = 7


class RequestRequiresAuthentication(APIErrorException):
    ERROR_CODE = 8


class RequestRequiresPermission(APIErrorException):
    """
    Returned when a request requires a certain permission that has not been granted for this plugin.
    """
    ERROR_CODE = 9


# Errors related to AuthenticationTokenRequest

class TokenRequestDenied(APIErrorException):
    ERROR_CODE = 50


class TokenRequestCurrentlyOngoing(APIErrorException):
    ERROR_CODE = 51


class TokenRequestPluginNameInvalid(APIErrorException):
    ERROR_CODE = 52


class TokenRequestDeveloperNameInvalid(APIErrorException):
    ERROR_CODE = 53


class TokenRequestPluginIconInvalid(APIErrorException):
    ERROR_CODE = 54


# Errors related to AuthenticationRequest

class AuthenticationTokenMissing(APIErrorException):
    ERROR_CODE = 100


class AuthenticationPluginNameMissing(APIErrorException):
    ERROR_CODE = 101


class AuthenticationPluginDeveloperMissing(APIErrorException):
    ERROR_CODE = 102


# Errors related to ModelLoadRequest

class ModelIDMissing(APIErrorException):
    ERROR_CODE = 150


class ModelIDInvalid(APIErrorException):
    ERROR_CODE = 151


class ModelIDNotFound(APIErrorException):
    ERROR_CODE = 152


class ModelLoadCooldownNotOver(APIErrorException):
    ERROR_CODE = 153


class CannotCurrentlyChangeModel(APIErrorException):
    ERROR_CODE = 154


# Errors related to HotkeyTriggerRequest

class HotkeyQueueFull(APIErrorException):
    """
    Only a certain amount of hotkey activations can be queued until you have to wait for execution completion.
    """
    ERROR_CODE = 200


class HotkeyExecutionFailedBecauseNoModelLoaded(APIErrorException):
    ERROR_CODE = 201


class HotkeyIDNotFoundInModel(APIErrorException):
    ERROR_CODE = 202


class HotkeyCooldownNotOver(APIErrorException):
    """
    Individual hotkeys have a global 5 second cooldown
    """
    ERROR_CODE = 203


class HotkeyIDFoundButHotkeyDataInvalid(APIErrorException):
    """
    For example missing files for expression/animation hotkey
    """
    ERROR_CODE = 204


class HotkeyExecutionFailedBecauseBadState(APIErrorException):
    """
    For example when trying to load a model and the user has certain config windows open that temporarily prevent that
    """
    ERROR_CODE = 205


class HotkeyUnknownExecutionFailure(APIErrorException):
    ERROR_CODE = 206


class HotkeyExecutionFailedBecauseLive2DItemNotFound(APIErrorException):
    """
    When triggering hotkeys in Live2D items, this will be returned if the requested Live2D item has not been found.
    """
    ERROR_CODE = 207


class HotkeyExecutionFailedBecauseLive2DItemsDoNotSupportThisHotkeyType(APIErrorException):
    """
    Only a subset of hotkey actions are supported in Live2D items, for example Expression hotkeys.
    """
    ERROR_CODE = 208


# Errors related to ColorTintRequest

class ColorTintRequestNoModelLoaded(APIErrorException):
    ERROR_CODE = 250


class ColorTintRequestMatchOrColorMissing(APIErrorException):
    ERROR_CODE = 251


class ColorTintRequestInvalidColorValue(APIErrorException):
    ERROR_CODE = 252


# Errors related to MoveModelRequest

class MoveModelRequestNoModelLoaded(APIErrorException):
    ERROR_CODE = 300


class MoveModelRequestMissingFields(APIErrorException):
    ERROR_CODE = 301


class MoveModelRequestValuesOutOfRange(APIErrorException):
    ERROR_CODE = 302


# Errors related to ParameterCreationRequest

class CustomParamNameInvalid(APIErrorException):
    ERROR_CODE = 350


class CustomParamValuesInvalid(APIErrorException):
    ERROR_CODE = 351


class CustomParamAlreadyCreatedByOtherPlugin(APIErrorException):
    ERROR_CODE = 352


class CustomParamExplanationTooLong(APIErrorException):
    ERROR_CODE = 353


class CustomParamDefaultParamNameNotAllowed(APIErrorException):
    """
    When you use names of default param names, like MouthX, FaceAngleZ, MouthSmile, ...
    """
    ERROR_CODE = 354


class CustomParamLimitPerPluginExceeded(APIErrorException):
    ERROR_CODE = 355


class CustomParamLimitTotalExceeded(APIErrorException):
    ERROR_CODE = 356


# Errors related to ParameterDeletionRequest

class CustomParamDeletionNameInvalid(APIErrorException):
    ERROR_CODE = 400


class CustomParamDeletionNotFound(APIErrorException):
    """
    Trying to delete a parameter that doesn't exist
    """
    ERROR_CODE = 401


class CustomParamDeletionCreatedByOtherPlugin(APIErrorException):
    """
    Trying to delete a parameter created by another plugin
    """
    ERROR_CODE = 402


class CustomParamDeletionCannotDeleteDefaultParam(APIErrorException):
    ERROR_CODE = 403


# Errors related to InjectParameterDataRequest

class InjectDataNoDataProvided(APIErrorException):
    ERROR_CODE = 450


class InjectDataValueInvalid(APIErrorException):
    ERROR_CODE = 451


class InjectDataWeightInvalid(APIErrorException):
    ERROR_CODE = 452


class InjectDataParamNameNotFound(APIErrorException):
    """
    Trying to send data for parameter that doesn't exist
    """
    ERROR_CODE = 453


class InjectDataParamControlledByOtherPlugin(APIErrorException):
    """
    Only one plugin can send data for a parameter at a time
    """
    ERROR_CODE = 454


class InjectDataModeUnknown(APIErrorException):
    """
    Only "add" and "set" can be used. If no mode is provided, "set" will be used.
    """
    ERROR_CODE = 455


# Errors related to ParameterValueRequest

class ParameterValueRequestParameterNotFound(APIErrorException):
    ERROR_CODE = 500


# Errors related to NDIConfigRequest

class NDIConfigCooldownNotOver(APIErrorException):
    ERROR_CODE = 550


class NDIConfigResolutionInvalid(APIErrorException):
    ERROR_CODE = 551


# Errors related to ExpressionStateRequest

class ExpressionStateRequestInvalidFilename(APIErrorException):
    ERROR_CODE = 600


class ExpressionStateRequestFileNotFound(APIErrorException):
    ERROR_CODE = 601


# Errors related to ExpressionStateRequest

class ExpressionActivationRequestInvalidFilename(APIErrorException):
    ERROR_CODE = 650


class ExpressionActivationRequestFileNotFound(APIErrorException):
    ERROR_CODE = 651


class ExpressionActivationRequestNoModelLoaded(APIErrorException):
    ERROR_CODE = 652


# Errors related to SetCurrentModelPhysicsRequest

class SetCurrentModelPhysicsRequestNoModelLoaded(APIErrorException):
    ERROR_CODE = 700


class SetCurrentModelPhysicsRequestModelHasNoPhysics(APIErrorException):
    ERROR_CODE = 701


class SetCurrentModelPhysicsRequestPhysicsControlledByOtherPlugin(APIErrorException):
    ERROR_CODE = 702


class SetCurrentModelPhysicsRequestNoOverridesProvided(APIErrorException):
    ERROR_CODE = 703


class SetCurrentModelPhysicsRequestPhysicsGroupIDNotFound(APIErrorException):
    ERROR_CODE = 704


class SetCurrentModelPhysicsRequestNoOverrideValueProvided(APIErrorException):
    ERROR_CODE = 705


class SetCurrentModelPhysicsRequestDuplicatePhysicsGroupID(APIErrorException):
    ERROR_CODE = 706


# Errors related to ItemLoadRequest

class ItemFileNameMissing(APIErrorException):
    ERROR_CODE = 750


class ItemFileNameNotFound(APIErrorException):
    ERROR_CODE = 751


class ItemLoadLoadCooldownNotOver(APIErrorException):
    """
    Not used anymore. The cooldown for loading items has been removed.
    """
    ERROR_CODE = 752


class CannotCurrentlyLoadItem(APIErrorException):
    """
    This is usually because the user has menus open that prevent items from being loaded.
    """
    ERROR_CODE = 753


class CannotLoadItemSceneFull(APIErrorException):
    ERROR_CODE = 754


class ItemOrderInvalid(APIErrorException):
    ERROR_CODE = 755


class ItemOrderAlreadyTaken(APIErrorException):
    ERROR_CODE = 756


class ItemLoadValuesInvalid(APIErrorException):
    """
    Invalid values for fields like size, position, ...
    """
    ERROR_CODE = 757


class ItemCustomDataInvalid(APIErrorException):
    """
    Invalid values for custom data field (customDataBase64). Happens when data is provided here but it's no valid JPG/PNG data or image dimensions are invalid.
    """
    ERROR_CODE = 758


class ItemCustomDataCannotAskRightNow(APIErrorException):
    """
    Max. number of item load prompts are already currently shown to the user.
    """
    ERROR_CODE = 759


class ItemCustomDataLoadRequestRejectedByUser(APIErrorException):
    """
    You requested a custom data image item to be loaded but the user rejected it.
    """
    ERROR_CODE = 760


# Errors related to ItemUnloadRequest

class CannotCurrentlyUnloadItem(APIErrorException):
    """
     This is usually because the user has menus open that prevent items from being unloaded.
    """
    ERROR_CODE = 800


# Errors related to ItemAnimationControlRequest

class ItemAnimationControlInstanceIDNotFound(APIErrorException):
    ERROR_CODE = 850


class ItemAnimationControlUnsupportedItemType(APIErrorException):
    """
    Returned when trying to use this request for Live2D items.
    """
    ERROR_CODE = 851


class ItemAnimationControlAutoStopFramesInvalid(APIErrorException):
    """
    Auto-stop frames indices have to be between 0 and the last frame index of the animated item.
    """
    ERROR_CODE = 852


class ItemAnimationControlTooManyAutoStopFrames(APIErrorException):
    """
    Maximum allowed number per item is 1024.
    """
    ERROR_CODE = 853


class ItemAnimationControlSimpleImageDoesNotSupportAnim(APIErrorException):
    """
    You can set stuff like transparency and brightness for normal PNG/JPG items, but nothing animation-related.
    """
    ERROR_CODE = 854


# Errors related to ItemMoveRequest

class ItemMoveRequestInstanceIDNotFound(APIErrorException):
    ERROR_CODE = 900


class ItemMoveRequestInvalidFadeMode(APIErrorException):
    ERROR_CODE = 901


class ItemMoveRequestItemOrderTakenOrInvalid(APIErrorException):
    ERROR_CODE = 902


class ItemMoveRequestCannotCurrentlyChangeOrder(APIErrorException):
    """
    Cannot change order when any windows are open.
    """
    ERROR_CODE = 903


# Errors related to EventSubscriptionRequest

class EventSubscriptionRequestEventTypeUnknown(APIErrorException):
    ERROR_CODE = 950


# Errors related to ArtMeshSelectionRequest

class ArtMeshSelectionRequestNoModelLoaded(APIErrorException):
    """
    Cannot start request because no model is loaded.
    """
    ERROR_CODE = 1000


class ArtMeshSelectionRequestOtherWindowsOpen(APIErrorException):
    """
    Other windows are currently open, can't start request.
    """
    ERROR_CODE = 1001


class ArtMeshSelectionRequestModelDoesNotHaveArtMesh(APIErrorException):
    """
    At least one of the "active" ArtMeshes you provided does not exist in the model.
    """
    ERROR_CODE = 1002


class ArtMeshSelectionRequestArtMeshIDListError(APIErrorException):
    """
    Your "active" ArtMesh ID list is too long.
    """
    ERROR_CODE = 1003


# Errors related to ItemPinRequest

class ItemPinRequestGivenItemNotLoaded(APIErrorException):
    ERROR_CODE = 1050


class ItemPinRequestInvalidAngleOrSizeType(APIErrorException):
    ERROR_CODE = 1051


class ItemPinRequestModelNotFound(APIErrorException):
    ERROR_CODE = 1052


class ItemPinRequestArtMeshNotFound(APIErrorException):
    ERROR_CODE = 1053


class ItemPinRequestPinPositionInvalid(APIErrorException):
    ERROR_CODE = 1054


# Errors related to PermissionRequest

class PermissionRequestUnknownPermission(APIErrorException):
    ERROR_CODE = 1100


class PermissionRequestCannotRequestRightNow(APIErrorException):
    """
    Permission config window is open.
    """
    ERROR_CODE = 1101


class PermissionRequestFileProblem(APIErrorException):
    """
    Could not open or write permission file for this plugin.
    """
    ERROR_CODE = 1102


# Errors related to PostProcessingListRequest

class PostProcessingListRequestInvalidFilter(APIErrorException):
    """
    Provided filter array too long (more than 512 entries)
    """
    ERROR_CODE = 1150


# Errors related to PostProcessingUpdateRequest

class PostProcessingUpdateRequestCannotUpdateRightNow(APIErrorException):
    """
    Cannot update post-processing when windows are open.
    """
    ERROR_CODE = 1200


class PostProcessingUpdateRequestFadeTimeInvalid(APIErrorException):
    ERROR_CODE = 1201


class PostProcessingUpdateRequestLoadingPresetAndValues(APIErrorException):
    """
    Cannot load preset and individual config values with one request. Do one or the other.
    """
    ERROR_CODE = 1202


class PostProcessingUpdateRequestPresetFileLoadFailed(APIErrorException):
    """
    Requested preset file was not found in the "Effects" folder.
    """
    ERROR_CODE = 1203


class PostProcessingUpdateRequestValueListInvalid(APIErrorException):
    ERROR_CODE = 1204


class PostProcessingUpdateRequestValueListContainsDuplicates(APIErrorException):
    ERROR_CODE = 1205


class PostProcessingUpdateRequestTriedToLoadRestrictedEffect(APIErrorException):
    """
    Tried to configure a restricted effect but user doesn't have those effects enabled/allowed.
    """
    ERROR_CODE = 1206


class UnknownError(APIErrorException):
    ERROR_CODE = -1

    def __init__(self, error_message: str, error_code: int = 0):
        logger.warning(f"Unknown error from API. Create new issue if you can't see any of them for this error. {f'Error code: {error_code} ' if error_code else ''} Error message: {error_message}")
        self.error_message = error_message
