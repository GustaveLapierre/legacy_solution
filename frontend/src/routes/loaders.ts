export async function RecordsLoader({ request }: { request: Request }) {
    return fetch("/api/records", {
        signal: request.signal
    })
}

export async function SingleRecordLoader({request, params}: {request: Request, params: any}) {
    const res = await fetch(`/api/get-record/${params.id}`, {
        signal: request.signal
    })
    if (res.status === 404)  throw new Response("Not Found", {status: 404})
    return res.json()
}

export async function ProfileLoader({ request }: { request: Request }) {
    return fetch("/api/profile", {
        signal: request.signal
    })
}