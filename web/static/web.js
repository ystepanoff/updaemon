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
        saveSourceButton.click(function () {
            let params = $('#sourceParams').val().toString();
            try {
                $.parseJSON(params);
                $.post(
                    "/source",
                    {
                        "source_id": $('#sourceId').val().toString(),
                        "name": $('#sourceName').val().toString(),
                        "description": $('#sourceDescription').val().toString(),
                        "remote": $('#sourceRemote').val().toString(),
                        "scraper_id": $('#sourceScraperId').val().toString(),
                        "params": params
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
            } catch (exception) {
                alert(exception.toString());
            }
        });
        $('#sourceScraperId').change(function () {
            for
        });
    }

    for (let actionModal of actionModals) {
        let modal = $('#' + actionModal.id)
        let parts = actionModal.id.split('-');
        let source_action_id = parseInt(parts[1]);
        modal.find('#cancelSaveActionIcon-' + source_action_id).click(() => modal.removeClass('is-active'));
        modal.find('#cancelSaveAction-' + source_action_id).click(() => modal.removeClass('is-active'));
        modal.find('#saveAction-' + source_action_id).click(function () {
            let paramsTable = modal.find('#actionParamsTable-' + source_action_id);
            let params = {};
            for (let inputField of paramsTable.find(':input')) {
                params[inputField.name] = inputField.value
            }
            $.post(
                "/action",
                {
                    "source_id": $('#sourceId').val().toString(),
                    "action_id": modal.find('#actionId').val(),
                    "source_action_id": source_action_id,
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
            let source_action_id = parseInt(parts[1]);
            // TODO: params validation
            let params_config = $('#actionParamsConfig-' + source_action_id).val();
            let modal = $('#actionModal-' + source_action_id)
            modal.addClass('is-active');
        });
    }

    if (addSourceButton.length) {
        let modal = $('#addSourceModal');
        modal.find('#addSourceCancel').click(() => modal.removeClass('is-active'));
        modal.find('#addSourceCancelIcon').click(() => modal.removeClass('is-active'));
        addSourceButton.click(function () {
            modal.addClass('is-active');
        });
        modal.find('#addSourceSave').click(function () {
            let name = modal.find('#addSourceName').val();
            let description = modal.find('#addSourceDescription').val();
            let remote = modal.find('#addSourceRemote').val();
            let scraper_id = modal.find('#addSourceScraperId').val();
            let params = modal.find('#addSourceParams').val();
            try {
                $.parseJSON(params);
                $.post(
                    "/source",
                    {
                        "name": name,
                        "description": description,
                        "remote": remote,
                        "scraper_id": scraper_id,
                        "params": params
                    },
                    () => modal.removeClass('is-active')
                ).done(() => location.reload()).fail(function (xhr, status, error) {
                    alert(error);
                    modal.removeClass('is-active');
                });
            } catch (exception) {
                alert(exception.toString());
            }
        });
    }

    for (let deleteSourceButton of deleteSourceButtons) {
        $('#' + deleteSourceButton.id).click(function () {
            if (confirm("Do you want to delete this source?")) {
                let parts = deleteSourceButton.id.split('-');
                let source_id = parseInt(parts[1]);
                $.post(
                    "/source",
                    {
                        "source_id": source_id,
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
                let source_action_id = parseInt(parts[1]);
                $.post(
                    "/action",
                    {
                        "source_id": $('#sourceId').val().toString(),
                        "source_action_id": source_action_id,
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
        modal.find('#addActionSave').click(function () {
            let baseClassId = parseInt(modal.find('#addActionBaseClass').val());
            let paramsTable = modal.find('#addActionParamsTable-' + baseClassId);
            let params = {};
            for (let inputField of paramsTable.find(':input')) {
                params[inputField.name] = inputField.value
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