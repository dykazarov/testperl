#!/usr/bin/env perl
use strict;
use warnings;

my $LINELIMIT = 100;

use CGI;

my $q = CGI::new;

my $id = $q->param( "dstaddr" );

print $q->header(
    -type    => 'text/html',
    -charset => 'utf-8',
);

if( ! defined($id) )
{
    print
	$q->start_html('Get log of recipient.'),
	$q->start_form,
	q{Enter recipient's address: },
	$q->textfield('dstaddr'),
	$q->submit,
	$q->end_form,
	$q->end_html;
}
else
{
    print
	$q->start_html( 'Log records of recipient '. $id );

    use DBI;
    my $dbh = DBI->connect( "DBI:mysql:database=test;host=localhost", "user", "" ) or
	die 'Error connecting to to database: '.$DBI::errstr."\n";

    $dbh->do(
	    q{
		    create temporary table ttttt
		    select int_id, created, str from log where address = ?
		    union
		    select int_id, created, str from message where int_id in ( select distinct int_id from log where address = ? )
	    },
	    undef,
	    $id, $id
    ) or
	die 'Error collecting the data: '.$dbh->errstr()."\n";

    my $sth = $dbh->prepare( 'select created, str from ttttt order by int_id, created' ) or
	die 'Error preparing the data extraction: '.$dbh->errstr()."\n";
    $sth->execute or
	die 'Error executin the data extration: '.$dbh->errstr()."\n";

    my $cntr = 0;
    my @tbl;
    push @tbl, $q->Tr( undef, $q->th({'colspan'=>2},'Log') );

    while( ( my ($created, $str) = $sth->fetchrow_array ) ) {
	if( ++ $cntr > $LINELIMIT )
	{
	    push @tbl, $q->Tr( undef, $q->td({'colspan'=>2},'Too many lines found') );
	    last;
	}

	push @tbl, $q->Tr( undef, $q->td($created), $q->td($str) );
    }

    print
	$q->table( undef, @tbl ),
	$q->end_html;
}

exit(0);
