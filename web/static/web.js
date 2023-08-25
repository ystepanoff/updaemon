$(document).ready(function() {
    let saveSourceButton = $('#saveSourceButton');
    let addSourceButton = $('#addSourceButton');
    let deleteSourceButtons = $('[id^="deleteSourceButton-"]');
    let deleteActionButtons = $('[id^="deleteActionButton-"]');
    let configureActionButtons = $('[id^="configureActionButton-"]');
    let actionModals = $('[id^="actionModal-"]');
    let addActionButton = $('#addActionButton');

    if (saveSourceButton.length) {
        let saveSourceFailed = $('#saveSourceFailed');
        let saveSourceSuccess = $('#saveSourceSuccess');
        let sourceScraperId = $('#sourceScraperId').val();
        saveSourceButton.click(function () {
            let params = {};
            for (let inputField of $('#scraperParams-' + sourceScraperId).find(':input')) {
                params[inputField.name] = inputField.value;
            }
            $.post(
                "/source",
                {
                    "source_id": $('#sourceId').val(),
                    "name": $('#sourceName').val(),
                    "description": $('#sourceDescription').val(),
                    "remote": $('#sourceRemote').val(),
                    "scraper_id": $('#sourceScraperId').val(),
                    "params": JSON.stringify(params)
                },
                function () {
                    saveSourceSuccess.removeClass('is-hidden');
                    saveSourceSuccess.stop();
                    saveSourceSuccess.fadeTo(0, 1.0);
                    saveSourceSuccess.fadeOut(
                        5000,
                        function () {
                            saveSourceSuccess.addClass('is-hidden').fadeTo(0, 1.0);
                        }
                    );
                    saveSourceFailed.addClass('is-hidden').fadeTo(0, 1.0);
                }
            ).fail(function (xhr, status, error) {
                saveSourceFailed.removeClass('is-hidden');
                saveSourceFailed.stop();
                saveSourceFailed.fadeTo(0, 1.0);
                saveSourceFailed.fadeOut(
                    5000,
                    function () {
                        saveSourceFailed.addClass('is-hidden').fadeTo(0, 1.0);
                    }
                )
            });
        });
        $('#sourceScraperId').change(function () {
            for (let scraperParams of $('[id^="scraperParams-"]')) {
                let parts = scraperParams.id.split('-');
                let sourceScraperId = parseInt(parts[1]);
                if (sourceScraperId === parseInt($('#sourceScraperId').val())) {
                    $('#' + scraperParams.id).removeClass('is-hidden');
                } else {
                    $('#' + scraperParams.id).addClass('is-hidden');
                }
            }
        });
    }

    for (let actionModal of actionModals) {
        let modal = $('#' + actionModal.id)
        let parts = actionModal.id.split('-');
        let sourceActionId = parseInt(parts[1]);
        modal.find('#cancelSaveActionIcon-' + sourceActionId).click(() => modal.removeClass('is-active'));
        modal.find('#cancelSaveAction-' + sourceActionId).click(() => modal.removeClass('is-active'));
        modal.find('#saveAction-' + sourceActionId).click(function () {
            let paramsTable = modal.find('#actionParamsTable-' + sourceActionId);
            let paramsConfig = {}
            for (let paramConfig of modal.find('[id^="actionParamConfig-"]')) {
                let parts = paramConfig.id.split('-');
                paramsConfig[parts[1]] = paramConfig.value;
            }
            let params = {};
            for (let inputField of paramsTable.find(':input')) {
                if (inputField.type === "hidden") {
                    continue;
                }
                if (paramsConfig[inputField.name] === "list") {
                    params[inputField.name] = inputField.value.replace(/\s/g, '').split(',');
                } else {
                    params[inputField.name] = inputField.value;
                }
            }
            $.post(
                "/action",
                {
                    "source_id": $('#sourceId').val().toString(),
                    "action_id": modal.find('#actionId').val(),
                    "source_action_id": sourceActionId,
                    "params": JSON.stringify(params),
                },
                function () {
                    modal.removeClass('is-active');
                }
            ).done(() => location.reload()).fail(function (xhr, status, error) {
            });
        });
    }

    for (let configureActionButton of configureActionButtons) {
        $('#' + configureActionButton.id).click(function () {
            let parts = configureActionButton.id.split('-');
            let sourceActionId = parseInt(parts[1]);
            let modal = $('#actionModal-' + sourceActionId)
            modal.addClass('is-active');
        });
    }

    if (addSourceButton.length) {
        let modal = $('#addSourceModal');
        let scraperSelect = modal.find('#addSourceScraperId');
        let scraperId = parseInt(scraperSelect.val());
        for (let scraperParams of $('[id^="scraperParams-"]')) {
            let parts = scraperParams.id.split('-');
            let scraperParamsId = parseInt(parts[1]);
            if (scraperParamsId === scraperId) {
                $('#' + scraperParams.id).removeClass('is-hidden');
            }
        }
        modal.find('#addSourceCancel').click(() => modal.removeClass('is-active'));
        modal.find('#addSourceCancelIcon').click(() => modal.removeClass('is-active'));
        addSourceButton.click(function () {
            modal.addClass('is-active');
        });
        modal.find('#addSourceScraperId').change(function () {
            let newScraperId = parseInt(scraperSelect.val());
            for (let scraperParams of $('[id^="scraperParams-"]')) {
                let parts = scraperParams.id.split('-');
                let scraperParamsId = parseInt(parts[1]);
                if (scraperParamsId === newScraperId) {
                    $('#' + scraperParams.id).removeClass('is-hidden');
                } else {
                    $('#' + scraperParams.id).addClass('is-hidden');
                }
            }
        });
        modal.find('#addSourceSave').click(function () {
            let name = modal.find('#addSourceName').val();
            let description = modal.find('#addSourceDescription').val();
            let remote = modal.find('#addSourceRemote').val();
            let params = {};
            for (let inputField of $('#scraperParams-' + scraperSelect.val()).find(':input')) {
                params[inputField.name] = inputField.value;
            }
            $.post(
                "/source",
                {
                    "name": name,
                    "description": description,
                    "remote": remote,
                    "scraper_id": scraperSelect.val(),
                    "params": JSON.stringify(params)
                },
                () => modal.removeClass('is-active')
            ).done(() => location.reload()).fail(function (xhr, status, error) {
                alert(error);
                modal.removeClass('is-active');
            });
        });
    }

    for (let deleteSourceButton of deleteSourceButtons) {
        $('#' + deleteSourceButton.id).click(function () {
            if (confirm("Do you want to delete this source?")) {
                let parts = deleteSourceButton.id.split('-');
                let sourceId = parseInt(parts[1]);
                $.post(
                    "/source",
                    {
                        "source_id": sourceId,
                        "delete": true
                    },
                    () => location.reload()
                ).fail(function (xhr, status, error) {
                    alert(error);
                });
            }
        });
    }

    for (let deleteActionButton of deleteActionButtons) {
        $('#' + deleteActionButton.id).click(function () {
            if (confirm("Do you want to delete this action?")) {
                let parts = deleteActionButton.id.split('-');
                let sourceActionId = parseInt(parts[1]);
                $.post(
                    "/action",
                    {
                        "source_id": $('#sourceId').val().toString(),
                        "source_action_id": sourceActionId,
                        "delete": true
                    },
                    () => location.reload()
                ).fail(function (xhr, status, error) {
                    alert(error);
                });
            }
        });
    }

    if (addActionButton.length) {
        let modal = $('#addActionModal');
        modal.find('#addActionCancel').click(() => modal.removeClass('is-active'));
        modal.find('#addActionCancelIcon').click(() => modal.removeClass('is-active'));
        addActionButton.click(function () {
            modal.addClass('is-active');
        });
        for (let actionParamsTable of $('[id^="addActionParamsTable-"]')) {
            let parts = actionParamsTable.id.split('-');
            let baseClassId = parseInt(parts[1]);
            if (baseClassId === parseInt($('#addActionBaseClass').val())) {
                $('#' + actionParamsTable.id).removeClass('is-hidden');
            } else {
                $('#' + actionParamsTable.id).addClass('is-hidden');
            }
        }
        modal.find('#addActionSave').click(function () {
            let baseClassId = parseInt(modal.find('#addActionBaseClass').val());
            let paramsTable = modal.find('#addActionParamsTable-' + baseClassId);
            let paramsConfig = {};
            for (let paramConfig of paramsTable.find('[id^="addActionParamConfig-"]')) {
                let parts = paramConfig.id.split('-');
                paramsConfig[parts[1]] = paramConfig.value;
            }
            let params = {};
            for (let inputField of paramsTable.find(':input')) {
                if (inputField.type === "hidden") {
                    continue;
                }
                if (paramsConfig[inputField.name] === "list") {
                    params[inputField.name] = inputField.value.replace(/\s/g, '').split(',');
                } else {
                    params[inputField.name] = inputField.value;
                }
            }
            $.post(
                "/action",
                {
                    "source_id": $('#sourceId').val().toString(),
                    "action_id": baseClassId,
                    "params": JSON.stringify(params)
                },
                () => modal.removeClass('is-active')
            ).done(() => location.reload()).fail(function (xhr, status, error) {
                alert(error);
                modal.removeClass('is-active');
            });
        });
        modal.find('#addActionBaseClass').change(function () {
            for (let paramsTable of modal.find('[id^="addActionParamsTable-"]')) {
                if (!$('#' + paramsTable.id).hasClass('is-hidden')) {
                    $('#' + paramsTable.id).addClass('is-hidden');
                }
            }
            let baseClassId = parseInt(modal.find('#addActionBaseClass').val());
            modal.find('#addActionParamsTable-' + baseClassId).removeClass('is-hidden');
        });
    }
});
