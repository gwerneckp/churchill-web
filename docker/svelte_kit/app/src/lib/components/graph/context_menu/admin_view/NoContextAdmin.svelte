<script lang="ts">
	import SearchPerson from '$lib/components/graph/context_menu/SearchPerson.svelte';
	import AddPerson from '$lib/components/graph/context_menu/admin_view/AddPerson.svelte';
	import { fade } from 'svelte/transition';
	import { gql } from '@apollo/client';
	import { client } from '$lib/apolloClient';
	import { userStore } from '$lib/stores/userStore';
	import { focusedPersonId } from '$lib/stores/focusedStore';
	import type { Person } from '$lib/types/person';
	import type { Suggestion } from '$lib/types/suggestion';
	import { onMount } from 'svelte';
	import Id from '../Id.svelte';

	let searchResult: Person[] = [];
	let suggestion: string;

	function handleSearch() {
		focusedPersonId.set(searchResult[0].id);
	}

	const GET_SUGGESTIONS_QUERY = () => gql`
		query {
			suggestions(where: { dealtWith: false }) {
				id
				message
				date
				dealtWith
			}
		}
	`;

	function updateSuggestions() {
		client
			.query({
				query: GET_SUGGESTIONS_QUERY()
			})
			.then((result) => {
				console.log(result);
				suggestions = result.data.suggestions;
			});
	}
	let suggestions: Suggestion[] = [];
	onMount(() => {
		updateSuggestions();
	});

	const DEAL_WITH_SUGGESTION_MUTATION = (id: string) => gql`
		mutation {
			updateSuggestions(where: { id: "${id}" }, update: { dealtWith: true }) {
				suggestions {
				id
				}
			}
}
`;
	function dealWithSuggestion(id: string) {
		client
			.mutate({
				mutation: DEAL_WITH_SUGGESTION_MUTATION(id)
			})
			.then((result) => {
				if (result) {
					updateSuggestions();
				}
			});
	}
</script>

<!-- UI for admin -->
<div class="bg-base-200">
	<h1 class="text-2xl font-bold p-4">Context Menu</h1>
</div>
<div class="bg-base-300 h-full px-4 pt-4">
	<h2 class="text-xl font-bold">Disclaimer</h2>
	<p>
		Disclaimer: By using this website, you acknowledge and accept the disclaimer located
		<a class="underline" href="/disclaimer">here</a>.
	</p>

	<div class="py-3" />

	<h2 class="text-xl font-bold">Search Person</h2>
	<!-- <p>Search for a person to access their information.</p> -->
	<div class="py-1" />

	<!-- Search for a person -->
	<SearchPerson bind:searchResult />

	<div class="py-1" />
	{#if searchResult[0]}
		<button on:click={handleSearch} class="btn btn-block btn-accent"
			>Go to {searchResult[0].name}</button
		>
	{:else}
		<button tabindex="-1" aria-disabled="true" class="btn btn-block btn-disabled">No Results</button
		>
	{/if}

	<div class="py-3" />
	<h2 class="text-xl font-bold">Add Person</h2>
	<AddPerson />

	<div class="py-3" />
	{#if suggestions.length > 1}
		<h2 class="text-xl font-bold">Suggestions</h2>
		<div class="py-1" />
		<div class="h-60 overflow-y-auto">
			{#each suggestions as suggestion}
				<div class=" p-2 bg-base-100 rounded-lg">
					<p class="font-bold">{suggestion.date}</p>
					<Id id={suggestion.id} /> <br />
					<div class="py-1" />
					<div class="flex justify-between gap-3">
						<p class="break-words">{suggestion.message}</p>

						<button
							on:click={() => dealWithSuggestion(suggestion.id)}
							class="btn btn-sm btn-accent"
						>
							Dealt with
						</button>
					</div>
				</div>
				<div class="py-1" />
			{/each}
		</div>
	{/if}

	<div class="py-3" />

	<h2 class="text-xl font-bold">Notice</h2>
	<div class="py-1" />
	<p>
		This database is designed to track relationships between individuals within the school
		community. Please <b>do not log relationships with random people from outside of school</b>,
		that one dude you met at UCPA last summer should not be here.
	</p>
	<br />
	<p>
		Please <b>do not log about people in Year 10 or bellow.</b> The database should include only information
		about lycéean students.
	</p>
</div>
