<script lang="ts">
	import type { userData } from '$lib/stores/userStore';
	import { userStore } from '$lib/stores/userStore';
	import { onMount } from 'svelte';

	type JWTData = {
		raw?: string;
		header?: {
			alg: string;
			typ: string;
		};
		payload?: {
			iat: string;
			exp: number;
			sub: userData;
		};
	};

	function jwtDecode(rawJwt: string) {
		const validJWT: RegExp = /^[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9-_]+$/;

		validJWT.test(rawJwt) || console.error('Invalid JWT provided');

		let token: JWTData = {};
		token.raw = rawJwt;
		token.header = JSON.parse(window.atob(rawJwt.split('.')[0]));
		token.payload = JSON.parse(window.atob(rawJwt.split('.')[1]));
		return token;
	}

	let user: userData;
	onMount(() => {
		const rawJwt = document.cookie
			.split('; ')
			.find((row) => row.startsWith('jwt'))
			?.split('=')[1];

		if (!rawJwt) {
			console.log('No JWT found');
			window.location.href = '/access';
			return;
		}

		const jwt = jwtDecode(rawJwt || '');

		// redirect to login if not logged in
		if (!jwt?.payload) {
			console.error('No JWT payload found');
			window.location.href = '/access';
			// console.log(jwt);
		}

		user = jwt?.payload?.sub as userData;
		userStore.set(user);
	});
</script>

{#if user}
	<slot />
{:else}
	<div class="h-full w-full flex justify-center items-center">
		<span class="loading loading-spinner loading-lg" />
	</div>
{/if}
