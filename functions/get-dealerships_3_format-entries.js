/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
function main(params) {
    if (params.error) {
        return {
            "error": {
                "status": 500,
                "msg": "Something went wrong on the server",
                "params": params
            }

        };
    }

    if (!params.docs.length) {
        return {
            "error": {
                "status": 404,
                "msg": "The database is empty or state does not exist",
            }
        };
    }

    return {
        entries: params.docs.map(doc => {
            return {
                id: doc.id,
                city: doc.city,
                state: doc.state,
                st: doc.st,
                address: doc.address,
                zip: doc.zip,
                lat: doc.lat,
                long: doc.long,
                short_name: doc.short_name,
                full_name: doc.full_name
            }
        })
    };
}
